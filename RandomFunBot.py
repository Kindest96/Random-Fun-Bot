#!/usr/bin/env python3
import logging
import telebot as telegram
import yaml

def main(configpath, loglevel):
    
    with open(configpath, "r") as f:
        config = yaml.safe_load(f)
    
    logging.basicConfig(format="%(levelname)-7s [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=loglevel)
    logging,info(config)
    
    print(config)

if __name__ == "__main__":
    
    configpath = "./config.yaml"
    
    loglevel = logging.INFO
    
    main(configpath, loglevel)