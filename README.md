<!-- BEGIN_ANSIBLE_DOCS -->
<!--
Do not edit README.md directly!

This file is generated automatically by aar-doc and will be overwritten.

Please edit meta/argument_specs.yml instead.
-->
# ansible-proserver-oauth2-proxy

oauth2-proxy role for Proserver

## Supported Operating Systems

- Debian 12, 13
- Ubuntu 24.04, 22.04
- FreeBSD [Proserver](https://infrastructure.punkt.de/de/produkte/proserver.html)

## Role Arguments



Configures and runs oauth2-proxy for Proserver.

On Linux, the role can install the oauth2-proxy binary from GitHub releases; set `oauth2_proxy.install` to control this. On FreeBSD, installation is not performed by this role.

Multiple oauth2-proxy instances can be defined via `oauth2_proxy.config`; each key is a config name (e.g. `app1`, `app2`) and each value is a mapping that is merged with `oauth2_proxy.defaults`.

On FreeBSD the role uses supervisord to manage services; on Linux it uses systemd. The supervisord config path depends on the `supervisord` role (e.g. `supervisord.prefix.config`).

#### Options for `oauth2_proxy`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `version` | oauth2-proxy release version to install from GitHub (e.g. 7.7.1). Only used when `oauth2_proxy.install` is true (Linux). | str | no | 7.7.1 |
| `install` | Whether to install the oauth2-proxy binary from GitHub releases. Defaults to true on Linux and false on FreeBSD. | bool | no | {{ true if ansible_facts['system'] == 'Linux' else false }} |
| `prefix` | Paths for oauth2-proxy installation and config. | dict of 'prefix' options | no |  |
| `rewrite_keys` | Options affecting how config keys are rewritten (e.g. proxy_prefix). | dict | no | {"proxy_prefix": true} |
| `http_proxy` | Optional HTTP proxy URL. When set, the systemd unit gets HTTP_PROXY. | str | no |  |
| `defaults` | Default options applied to every entry in `oauth2_proxy.config`. Each config entry is merged with these defaults; per-config values override. | dict of 'defaults' options | no |  |
| `config` | Per-instance oauth2-proxy configuration. Each key is a config name (e.g. `app1`); each value must be a mapping that is merged with `oauth2_proxy.defaults`. Empty or non-mapping entries are skipped. For each entry, config files are written under `oauth2_proxy.prefix.opt/etc/<config_name>/`. | dict | no |  |
| `branding` | Branding used in sign-in and error templates. | dict of 'branding' options | no |  |

#### Options for `oauth2_proxy.prefix`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `opt` | Base directory for oauth2-proxy (binary and per-instance config under etc/). | str | no | /var/opt/oauth2_proxy |
| `bin` | Path to the oauth2-proxy executable. | str | no | {{ '/var/opt/oauth2_proxy/bin/oauth2_proxy' if ansible_facts['system'] == 'Linux' else '/usr/local/bin/oauth2-proxy' }} |

#### Options for `oauth2_proxy.defaults`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `upstreams` | List of upstream URLs for oauth2-proxy. | list of '' | no | ['http://[::]:0/'] |
| `request_logging` | Whether to enable request logging (e.g. no, true). | str | no | no |
| `email_domains` | Allowed email domains (empty means allow all). | list of '' | no | [] |
| `htpasswd_file` | Optional path to htpasswd file, or a dict of username => password for the role to generate the file from the htpasswd template. | raw | no |  |
| `cookie_expire` | Cookie expiration (e.g. 672h). | str | no | 672h |
| `cookie_refresh` | Cookie refresh interval. | str | no | 1h |
| `cookie_secure` | Set secure flag on cookie. | bool | no | True |
| `cookie_httponly` | Set httponly flag on cookie. | bool | no | True |
| `set_xauthrequest` | Whether to set X-Auth-Request-* headers. | bool | no | True |
| `proxy_prefix` | Proxy prefix path. | str | no | /proserver/iap |
| `templates` | Paths to Jinja2 templates for oauth2_proxy.ini, sign_in.html, error.html, and htpasswd. Defaults point to the role templates. | dict | no |  |

#### Options for `oauth2_proxy.branding`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `sign_in_header` | Optional HTML for the sign-in page header. | str | no |  |
| `footer` | Optional HTML for the footer on sign-in and error pages. | str | no |  |

## Dependencies
- supervisord
  - **Condition**: `ansible_facts['system'] == "FreeBSD"`

## Installation
Add this role to the requirements.yml of your playbook as follows:
```yaml
roles:
  - name: ansible-proserver-oauth2-proxy
    src: https://github.com/punktDe/ansible-proserver-oauth2-proxy
```

Afterwards, install the role by running `ansible-galaxy install -r requirements.yml`

## Example Playbook

```yaml
- hosts: all
  roles:
    - name: oauth2-proxy
```

<!-- END_ANSIBLE_DOCS -->
