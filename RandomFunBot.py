#!/usr/bin/env python3
import telebot as telegram
import yaml

def main():
    
    with open(configpath, "r") as f:
        config = yaml.safe_load(f)
    
    
    print(config)

if __name__ == "__main__":
    
    configpath = "./config.yaml"
    
    main(configpath)