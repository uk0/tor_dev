import os
import unittest

from pyptlib.client import ClientTransportPlugin
from pyptlib.config import EnvError, ProxyError, Config
from pyptlib.test.test_core import PluginCoreTestMixin

class testClient(PluginCoreTestMixin, unittest.TestCase):
    pluginType = ClientTransportPlugin

    def test_fromEnv_legit(self):
        """Legit environment"""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        self.plugin._loadConfigFromEnv()
        self.assertOutputLinesEmpty()

    def test_fromEnv_bad(self):
        """Missing TOR_PT_MANAGED_TRANSPORT_VER."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("ENV-ERROR ")

    def test_fromEnv_bad2(self):
        """Missing TOR_PT_CLIENT_TRANSPORTS."""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("ENV-ERROR ")

    def test_fromEnv_proxy_http_legit(self):
        """Legit enviornment, with http proxy"""
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "http://user:password@192.0.2.1:80" }

        os.environ = TEST_ENVIRON
        self.plugin.config = self.plugin._loadConfigFromEnv()
        self.assertOutputLinesEmpty()
        proxy = self.plugin.config.getProxy()
        self.assertEquals(proxy.geturl(), TEST_ENVIRON["TOR_PT_PROXY"])
        self.assertEquals(proxy.scheme, "http")
        self.assertEquals(proxy.hostname, "192.0.2.1")
        self.assertEquals(proxy.port, 80)
        self.assertEquals(proxy.path, "")
        self.assertEquals(proxy.query, "")
        self.assertEquals(proxy.fragment, "")
        self.assertEquals(proxy.username, "user")
        self.assertEquals(proxy.password, "password")

    def test_fromEnv_proxy_socks4a_legit(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "socks4a://user@192.0.2.1:1080" }

        os.environ = TEST_ENVIRON
        self.plugin.config = self.plugin._loadConfigFromEnv()
        self.assertOutputLinesEmpty()
        proxy = self.plugin.config.getProxy()
        self.assertEquals(proxy.geturl(), TEST_ENVIRON['TOR_PT_PROXY'])
        self.assertEquals(proxy.scheme, "socks4a")
        self.assertEquals(proxy.hostname, "192.0.2.1")
        self.assertEquals(proxy.port, 1080)
        self.assertEquals(proxy.path, "")
        self.assertEquals(proxy.query, "")
        self.assertEquals(proxy.fragment, "")
        self.assertEquals(proxy.username, "user")
        self.assertEquals(proxy.password, None)

    def test_fromEnv_proxy_socks5_legit(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "socks5://user:password@192.0.2.1:1080" }

        os.environ = TEST_ENVIRON
        self.plugin.config = self.plugin._loadConfigFromEnv()
        self.assertOutputLinesEmpty()
        proxy = self.plugin.config.getProxy()
        self.assertEquals(proxy.geturl(), TEST_ENVIRON['TOR_PT_PROXY'])
        self.assertEquals(proxy.scheme, "socks5")
        self.assertEquals(proxy.hostname, "192.0.2.1")
        self.assertEquals(proxy.port, 1080)
        self.assertEquals(proxy.path, "")
        self.assertEquals(proxy.query, "")
        self.assertEquals(proxy.fragment, "")
        self.assertEquals(proxy.username, "user")
        self.assertEquals(proxy.password, "password")

    def test_fromEnv_proxy_invalid_scheme(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "gopher://user:password@192.0.2.1:70" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("PROXY-ERROR ")

    def test_fromEnv_proxy_missing_scheme(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "user:password@192.0.2.1:70" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("PROXY-ERROR ")

    def test_fromEnv_proxy_missing_port(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "http://user:password@192.0.2.1" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("PROXY-ERROR ")

    def test_fromEnv_proxy_invalid_has_path(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "http://user:password@192.0.2.1/path/" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("PROXY-ERROR ")

    def test_fromEnv_proxy_invalid_has_socks4_passwd(self):
        TEST_ENVIRON = { "TOR_PT_STATE_LOCATION" : "/pt_stat",
                         "TOR_PT_MANAGED_TRANSPORT_VER" : "1",
                         "TOR_PT_CLIENT_TRANSPORTS" : "dummy",
                         "TOR_PT_PROXY" : "socks4a://user:password@192.0.2.1:1080" }

        os.environ = TEST_ENVIRON
        self.assertRaises(EnvError, self.plugin._loadConfigFromEnv)
        self.assertOutputLinesStartWith("PROXY-ERROR ")

if __name__ == '__main__':
    unittest.main()

