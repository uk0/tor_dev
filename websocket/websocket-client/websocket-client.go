// Tor websocket client transport plugin.
//
// Usage in torrc:
// 	UseBridges 1
// 	Bridge websocket X.X.X.X:YYYY
// 	ClientTransportPlugin websocket exec ./websocket-client
package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"net/url"
	"os"
	"os/signal"
	"sync"
	"syscall"

	"golang.org/x/net/websocket"

	"git.torproject.org/pluggable-transports/goptlib.git"
)

var ptInfo pt.ClientInfo

const ptMethodName = "websocket"
const bufSiz = 1500

// When a connection handler starts, +1 is written to this channel; when it
// ends, -1 is written.
var handlerChan = make(chan int)

func usage() {
	fmt.Printf("Usage: %s [OPTIONS]\n", os.Args[0])
	fmt.Printf("WebSocket client pluggable transport for Tor.\n")
	fmt.Printf("Works only as a managed proxy.\n")
	fmt.Printf("\n")
	fmt.Printf("  -h, --help    show this help.\n")
	fmt.Printf("  --log FILE    log messages to FILE (default stderr).\n")
	fmt.Printf("  --socks ADDR  listen for SOCKS on ADDR.\n")
}

func proxy(local *net.TCPConn, ws *websocket.Conn) {
	var wg sync.WaitGroup

	wg.Add(2)

	// Local-to-WebSocket read loop.
	go func() {
		buf := make([]byte, bufSiz)
		var err error
		for {
			n, er := local.Read(buf[:])
			if n > 0 {
				ew := websocket.Message.Send(ws, buf[:n])
				if ew != nil {
					err = ew
					break
				}
			}
			if er != nil {
				err = er
				break
			}
		}
		if err != nil && err != io.EOF {
			log.Printf("%s", err)
		}
		local.CloseRead()
		ws.Close()

		wg.Done()
	}()

	// WebSocket-to-local read loop.
	go func() {
		var buf []byte
		var err error
		for {
			er := websocket.Message.Receive(ws, &buf)
			if er != nil {
				err = er
				break
			}
			n, ew := local.Write(buf)
			if ew != nil {
				err = ew
				break
			}
			if n != len(buf) {
				err = io.ErrShortWrite
				break
			}
		}
		if err != nil && err != io.EOF {
			log.Printf("%s", err)
		}
		local.CloseWrite()
		ws.Close()

		wg.Done()
	}()

	wg.Wait()
}

func handleConnection(conn *pt.SocksConn) error {
	defer conn.Close()

	handlerChan <- 1
	defer func() {
		handlerChan <- -1
	}()

	var ws *websocket.Conn

	log.Printf("SOCKS request for %s", conn.Req.Target)
	destAddr, err := net.ResolveTCPAddr("tcp", conn.Req.Target)
	if err != nil {
		conn.Reject()
		return err
	}
	wsUrl := url.URL{Scheme: "ws", Host: conn.Req.Target}
	ws, err = websocket.Dial(wsUrl.String(), "", wsUrl.String())
	if err != nil {
		err = conn.Reject()
		return err
	}
	log.Printf("WebSocket connection to %s", ws.Config().Location.String())
	defer ws.Close()
	err = conn.Grant(destAddr)
	if err != nil {
		return err
	}

	proxy(conn.Conn.(*net.TCPConn), ws)

	return nil
}

func socksAcceptLoop(ln *pt.SocksListener) error {
	defer ln.Close()
	for {
		socks, err := ln.AcceptSocks()
		if err != nil {
			if e, ok := err.(*net.OpError); ok && e.Temporary() {
				continue
			}
			return err
		}
		go func() {
			err := handleConnection(socks)
			if err != nil {
				log.Printf("SOCKS from %s: %s", socks.RemoteAddr(), err)
			}
		}()
	}
	return nil
}

func startListener(addrStr string) (*pt.SocksListener, error) {
	ln, err := pt.ListenSocks("tcp", addrStr)
	if err != nil {
		return nil, err
	}
	go func() {
		err := socksAcceptLoop(ln)
		if err != nil {
			log.Printf("accept: %s", err)
		}
	}()
	return ln, nil
}

func main() {
	var logFilename string
	var socksAddrStr string
	var err error

	flag.Usage = usage
	flag.StringVar(&logFilename, "log", "", "log file to write to")
	flag.StringVar(&socksAddrStr, "socks", "127.0.0.1:0", "address on which to listen for SOCKS connections")
	flag.Parse()

	if logFilename != "" {
		f, err := os.OpenFile(logFilename, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Can't open log file %q: %s.\n", logFilename, err.Error())
			os.Exit(1)
		}
		log.SetOutput(f)
	}

	log.SetFlags(log.LstdFlags | log.LUTC)
	log.Printf("starting")
	ptInfo, err = pt.ClientSetup(nil)
	if err != nil {
		log.Printf("error in setup: %s", err)
		os.Exit(1)
	}

	listeners := make([]net.Listener, 0)
	for _, methodName := range ptInfo.MethodNames {
		switch methodName {
		case ptMethodName:
			ln, err := startListener(socksAddrStr)
			if err != nil {
				pt.CmethodError(ptMethodName, err.Error())
				break
			}
			pt.Cmethod(ptMethodName, ln.Version(), ln.Addr())
			log.Printf("listening on %s", ln.Addr().String())
			listeners = append(listeners, ln)
		default:
			pt.CmethodError(methodName, "no such method")
		}
	}
	pt.CmethodsDone()

	var numHandlers int = 0
	var sig os.Signal
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// wait for first signal
	sig = nil
	for sig == nil {
		select {
		case n := <-handlerChan:
			numHandlers += n
		case sig = <-sigChan:
		}
	}
	for _, ln := range listeners {
		ln.Close()
	}

	if sig == syscall.SIGTERM {
		return
	}

	// wait for second signal or no more handlers
	sig = nil
	for sig == nil && numHandlers != 0 {
		select {
		case n := <-handlerChan:
			numHandlers += n
		case sig = <-sigChan:
		}
	}
}
