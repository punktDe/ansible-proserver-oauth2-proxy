# ansible-proserver-oauth2-proxy
An Ansible role that sets up [oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy) on a Proserver.

## Dependencies
[ansible-proserver-supervisord](https://github.com/punktDe/ansible-proserver-supervisord) is required to manage the service on FreeBSD

## FAQ
Q: Ansible crashes on macOS when trying to use the role

A: Add the following environment variable to your shell: `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

## Configuration options
### version
The oauth2-proxy version to be installed. You can see the available verions [here](https://github.com/oauth2-proxy/oauth2-proxy/tags)

**Default:**
```yaml
oauth2_proxy:
  version: 7.5.1
```

### install
Whether the oauth2-proxy binary should actually be installed. Change to `no` or `false` if you'd like to manage the binary yourself.

**Default:**
```yaml
oauth2_proxy:
  install: true
```

### prefix
Manages the location of the oauth2-proxy binary and configuration files, as well as the name of the binary file.

**Default:**
```yaml
oauth2_proxy:
  prefix:
    opt: /var/opt/oauth2_proxy
    binary: oauth2_proxy
```


### http_proxy
The address of the HTTP proxy to be used to access the Internet. Only supported on Linux installations

**Default:**
```yaml
oauth2_proxy:
  http_proxy:
```

### defaults
The default options for the oauth2-proxy config file (oauth2_proxy.ini). Most of the time, you'll probably want to use the `config` dict to configure your services instead.

**Default:**
```yaml
oauth2_proxy:
  defaults:
    upstreams: ["http://[::]:0/"]
    request_logging: no
    email_domains: []
    htpasswd_file:
    cookie_expire: "672h"
    cookie_refresh: "1h"
    cookie_secure: yes
    cookie_httponly: yes
    set_xauthrequest: yes
    proxy_prefix: /proserver/iap
    templates:
      oauth2_proxy.ini: "{{ role_path + '/templates/oauth2_proxy/oauth2_proxy.ini.j2' }}"
      sign_in.html: "{{ role_path + '/templates/oauth2_proxy/sign_in.html.j2' }}"
      error.html: "{{ role_path + '/templates/oauth2_proxy/error.html.j2' }}"
      htpasswd: "{{ role_path + '/templates/oauth2_proxy/htpasswd.j2' }}"
```

### config
A dictionary that consists of server configurations in the following format:

```yaml
oauth2_proxy:
  config:
    oidc:
      upstreams: ["http://[::]:4019"]
      provider: oidc
    gitlab:
      upstreams: ["http://[::]:4018"]
      provider: gitlab
```

Please consult the [official documentation](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview#command-line-options) for a full list of options (the "Command Line Options" section). The CLI options can be converted to config file options by removing the two leading dashes and replacing any dashes in the option name with underscores. For example, `--acr-values` -> `acr_values`.

For each configuration, a separate oauth2-proxy instance will be launched, so make sure that the upstream addresses don't overlap.

Likewise, each configuration is managed by its own separate supervisord/systemd service. For systemd, the service name is `oauth2-proxy@<config-name>.service`. whereas for supervisord, the name is `OAuth2Proxy<CapitalizedConfigName>`.

**Default:**
```yaml
oauth2_proxy:
  config: {}
```


### branding

Allows you to add custom HTML to the header and the footer of the oauth2-proxy sign-in page. For example:

```yaml
oauth2_proxy:
  branding:
    sign_in_header: >
      <img src="https://example.com/your-company-logo.png" width="200px"/>
    footer: >
      <a href="https://punkt.de">punkt.de</a> OAuth2 Proxy v{% raw %}{{.Version}}{% endraw %}
```

**Default:**
```yaml
oauth2_proxy:
  branding:
    sign_in_header:
    footer:
```
