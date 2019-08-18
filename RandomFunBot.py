#!/usr/bin/env python3
import logging
import telebot as telegram
import yaml

def main():
    
    with open(configpath) as f:
        config = yaml.safe_load(f)
    
    logging.info(config)

if __name__ == "__main__":
    
    configpath = "./config.yaml"
    
    main(configpath)