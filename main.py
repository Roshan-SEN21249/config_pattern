from parser_module.parser import Parser
from parser_module.ac_configs import config_cfpb, config_hpra

if __name__ == "__main__":
    p = Parser(config_cfpb)
    meta_data = p.analyser()
    print(meta_data)
