from distutils.core import setup
import py2exe

options = {"py2exe":  
                  {"compressed": 1,  
                    "optimize": 2,
                    "bundle_files": 1 
                   }  
                }
 
setup(console=['Bot.py'],
          options = options,
)