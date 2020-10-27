import argparse
import time
from discord import Status
from discord import Game
from discord.ext.commands import Bot

from story import init_model
from story import run_model

start_time = time.time()

parser = argparse.ArgumentParser(description='Input argument parser.')

parser.add_argument('--token', type=str, help='Bot token. Do not share this!')
parser.add_argument('--prefix', type=str, help='Prefix for interacting with the bot.', default='y!')
parser.add_argument('--context', type=str, help='Context string that is prefixed in every Act statement. It is filled with information that the AI should remember. This information is needed if you wish to inquire the AI about topics that haven\'nt been trained into it\'s model.',
        default='Nuwardia is a chatroom on a chat service called Discord that is a tight-knit community filled with friends. Nuwardia is filled with a group of friends that talk about topics ranging from technology to politics. Usually, there are some debates that occur in Nuwardia but it isn\'t too bad. You are relaxing one day when Yukari decided to materialize in your room. Yukari\'s intentions are solely to have a friendly conversation with you while you are relaxing in your room. You engage in conversation with Yukari.')

parser.add_argument('--model_dir', type=str, help='path of model folder')
parser.add_argument('--custom_model', type=str, help='path to custom model')
parser.add_argument('--nucleus', help='flag to turn on/off nucleus sampling', action='store_true')
parser.add_argument('--top_p', type=float, help='cut off probablity for nucleus sampling', default=1.0)
parser.add_argument('--top_k', type=int, help='cut off ranking for top K sampling', default=20)
parser.add_argument('--temperature', type=float, help='temperature in text generation. Higher temperature creates more randomness in the results.', default=0.2)
parser.add_argument('--batch_size', type=int, help='batch size', default=1)
parser.add_argument('--output_length', type=int, help='length of output sequence (number of tokens)', default=50)

args = parser.parse_args()

client = Bot(command_prefix=args.prefix)

def trunc(num, digits):
        sp = str(num).split('.')
        return '.'.join([sp[0], sp[1][:digits]])

def log(com, logstr):
        timestamp = time.time() - start_time
        print('[' + trunc(timestamp, 4) + '] ' + com + ': ' + logstr)

def actjob(message):
        log('ai  ', 'Processing Act job -- [' + message + ']')
        return run_model(args, args.context + message + '\n')

@client.event
async def on_ready():
        log('init', 'Connected to Discord servers.')
        game = Game('with Ran\'s tails~')
        await client.change_presence(status=Status.online, activity=game)

@client.command(name='reset',
                description='Resets AI execution. This is useful if you want to start the AI over from the beginning.',
                brief='Resets the AI model.',
                aliases=['r'],
                pass_context=True)
async def resetcmd(context):
        await context.message.channel.send("Standby... This will take a while...")
        log('ai  ', 'Restarting AI inferencer...')
        # reset AI here
        log('ai  ', 'Done!~')
        await context.message.channel.send("Done!~")

@client.command(name='say',
                description='Say something to Yukari!',
                brief='Say something to Yukari!',
                aliases=['s'],
                pass_context=True)
async def saycmd(context):
        message = " You say, \"" + context.message.content[6:] + "\""

        await context.message.channel.send(actjob(message))

@client.command(name='do',
                decsription='Do something to Yukari!',
                brief='Do something to Yukari!',
                aliases=['d'],
                pass_context=True)
async def docmd(context):
        message = context.message.content[5:]
        message = " You " + message[0].lower() + message[1:]
        if message[-1:] != '.':
                message = message + '.'

        await context.message.channel.send(actjob(message))

def main():
        if not args.token:
                print('token must be provided')
                exit()

        log('init', 'Server started at ' + time.strftime("%Y-%m-%d %H:%M"))
        log('init', 'Initializing model inferencer')
        init_model(args)
        client.run(args.token)

if __name__ == '__main__':
        main()