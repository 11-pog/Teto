import asyncio
import os
import sys
from unidecode import unidecode
import zc.lockfile

from resources_path import resources_path


class Utils:
    @staticmethod
    def is_duplicate(lock_name):
        try:
            lock = zc.lockfile.LockFile(lock_name)
            return lock
        except zc.lockfile.LockError:
            return None
    
    @staticmethod
    async def has_terminal():
        return sys.stdout is not None
    
    @staticmethod
    async def get_the_forbidden_list():
        path = os.path.join(resources_path('text'), 'the_big_forbidden_list_of_bad_words.txt')
        with open(path, 'r') as file:
            forbidden_list = file.read().split(',')
            forbidden_list = IterUtils.for_each_item(forbidden_list, StringUtils.clean)
            
            return forbidden_list



class StringUtils:
    @staticmethod
    def split_all(iter, sep):
        return [string.split(sep) for string in iter]
    
    @staticmethod
    def clean_all(iter):
        return [StringUtils.clean(msg) for msg in iter]
    
    @staticmethod
    def clean(msg):
        return unidecode(msg.lower().strip())



class IterUtils:
    @staticmethod
    def for_each_item(item_list, *actions):
        end_list = []
        
        for item in item_list:
            new_item = item
            
            for action in actions:
                new_item = action(new_item)
                
            end_list.append(new_item)
        
        return end_list
    
    @staticmethod
    def get_smallest_size(iter_of_iters):
        size = float('inf')
        for iter in iter_of_iters:
            if len(iter) < size:
                size = len(iter)
        return size




if __name__ == "__main__":
    john = ["PENIS", "PENIA MAIRO AINDA", "jonas pedro"]
    new_john = IterUtils.for_each_item(
        john,
        lambda item: item.split(' '),
        lambda word_list: 
            IterUtils.for_each_item(
                word_list,
                StringUtils.clean
                ),
        )
    pass