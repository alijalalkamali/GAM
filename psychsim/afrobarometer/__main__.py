import argparse
import configure
import os.path
import savReaderWriter
import world_initializer

from psychsim.world import *


# dir_path = os.path.dirname(os.path.realpath(__file__))
# ACTION_PATH = os.path.join(dir_path, 'action_list.txt')
# AGENT_PATH = os.path.join(dir_path, 'agent_list.txt')
# STATE_PATH = os.path.join(dir_path, 'state_list.txt')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from newsTexts.')
    parser.add_argument('--inputdir', '-i', required=True, help='input train file')
    parser.add_argument('--outputdir', '-o', default='outputs/', help='directory for outputs')
    args = parser.parse_args()
    
    with savReaderWriter.SavReader(args.inputdir) as reader:
        header = reader.header
        for line in reader:
            pass

    world = World()
    awi = world_initializer.AfroWorldInitializer(world)
    world.setOrder(world.agents.keys())
    result = world.step()
    world.explain(result, 5)