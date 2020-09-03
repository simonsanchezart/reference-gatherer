import sys
import os
from source import Source
from Services import Artstation, Pinterest, DeviantArt

def PrintUsage():
    print(f'Usage: referenceGather.py search term -service/s')
    # we get the id and name from all the sources
    for source in Source.GetSources():
        print(f'\t-{source.GetIdent()} {source.GetName()}')
    sys.exit()

# we will call this app from cmd at the folder we want to download images to
# we get the path from which cmd was called (script is in PATH)
# current working directory
cwd = os.getcwd()

art = Artstation()
pint = Pinterest()
dev = DeviantArt()

if len(sys.argv) < 2:
    PrintUsage()

# we split all the argv at ' -' to indicate a service
terms = ' '.join(sys.argv[1:]).split(' -')
searchTerm = terms[0]
servicesTerm = terms[1:]

if not servicesTerm:
    PrintUsage()

# we make a directory to hold all the images
folder = os.path.join(cwd, searchTerm)
os.makedirs(folder, exist_ok=True)

if art.GetIdent() in servicesTerm:
    art.Download(searchTerm, folder)
if pint.GetIdent() in servicesTerm:
    pint.Download(searchTerm, folder)
if dev.GetIdent() in servicesTerm:
    dev.Download(searchTerm, folder)
