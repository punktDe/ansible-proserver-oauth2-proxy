from hashlib import md5

def _merge_defaults(defaults, config):
    for key, default in defaults.items():
        if key == 'htpasswd':
            continue
        elif key == 'templates' and key in config:
            config[key] = _merge_defaults(defaults[key], config[key])
        elif key not in config:
            config[key] = default
    return config


def oauth2_proxy_templates(oauth2_proxy):
    files_to_template = []
    for config_name, config in oauth2_proxy['config'].items():
        if not config:
            continue

        config = _merge_defaults(oauth2_proxy['defaults'], config)

        config['custom_templates_dir'] = '{}/etc/{}'.format(oauth2_proxy['prefix']['opt'], config_name)
        for template_name, template_path in config['templates'].items():
            template_config = config.copy()

            del template_config['templates']

            if 'htpasswd_file' in template_config:
                if not template_config['htpasswd_file']:
                    del template_config['htpasswd_file']
                elif template_config['htpasswd_file'].__class__.__name__ == 'dict' and template_name == 'oauth2_proxy.ini':
                    template_config['htpasswd_file'] = '{}/etc/{}/htpasswd'.format(oauth2_proxy['prefix']['opt'], config_name)

            if 'cookie_name' not in template_config:
                template_config['cookie_name'] = 'psOA2{}'.format(md5(config_name.encode('utf-8')).hexdigest()[:5])

            files_to_template.append({
                    'src': template_path,
                    'dest': '{}/etc/{}/{}'.format(oauth2_proxy['prefix']['opt'], config_name, template_name),
                    'config': template_config,
                })

    return files_to_template


class FilterModule(object):
    def filters(self):
        return {
            'oauth2_proxy_templates': oauth2_proxy_templates,
        }
