import argparse
import ocdsdata.sources.all
import importlib
import os

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("--run", help="run one source only")
    parser.add_argument("--runall", help="run all sources",
                    action="store_true")
    parser.add_argument("--basedir", help="base dir - defaults to current directory")
    parser.add_argument("--outputdir", help="output dir - defaults to id. Ignored if running more than one runner.")

    args = parser.parse_args()

    run = []

    if args.runall:
        for sourceId, sourceInfo in ocdsdata.sources.all.SOURCES.items():
            sourceInfo['id'] = sourceId
            run.append(sourceInfo)
    elif args.run:
        if args.run in ocdsdata.sources.all.SOURCES:
            ocdsdata.sources.all.SOURCES[args.run]['id'] = args.run
            run.append(ocdsdata.sources.all.SOURCES[args.run])
        else:
            print("We can not find a source that you requested! You requested: %s" % [args.run])
            quit(-1)

    if not run:
        print("You have not specified anything to run! Try --run or --runall.")
        quit(-1)

    if args.verbose:
        print("We will run: ")
        for sourceInfo in run:
            print(" - %s" % sourceInfo['id'])

    base_dir = args.basedir or os.getcwd()
    remove_dir = False

    for sourceInfo in run:
        output_directory = sourceInfo['id']
        if len(run) == 1 and args.outputdir:
            output_directory = args.outputdir
            
        if args.verbose:
            print("Now running: %s (Output Dir: %s)" % (sourceInfo['id'], output_directory))

        module = importlib.import_module(sourceInfo['import'])
        class_ = getattr(module, sourceInfo['class'])
        instance = class_(base_dir, remove_dir, output_directory)
        instance.run_all()


if __name__ == '__main__':
    main()