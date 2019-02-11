import sys
sys.path.append("exchanges")
from exchange_modules import *
from ccxt_exchange import *

from time import *
from datetime import *
import configparser
import argparse

def processConfiguration(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)

	return {
		'apiKey' : config["API_KEYS"]["API_KEY"],
		'secret' : config["API_KEYS"]["SECRET_KEY"]
	}

def accountSummary(args):
	keyDict = processConfiguration(args.keys)
	coins = args.coins.split(",") if args.coins else None
	exchange = CCXTExchange(args.exchange, keyDict)
	
	accountBalance = exchange.getBalance()

	if coins:
		for coin in coins:
			print("{} : {}".format(coin, accountBalance[coin]))
	else:
		print(accountBalance)

def buyCoin(args):
	keyDict = processConfiguration(args.keys)
	coinPair = args.coinpair
	amount = args.amount
	exchange = CCXTExchange(args.exchange, keyDict)

	print(exchange.buyCoinPair(coinPair, amount))

def sellCoin(args):
	keyDict = processConfiguration(args.keys)
	coinPair = args.coinpair
	amount = args.amount
	exchange = CCXTExchange(args.exchange, keyDict)

	print(exchange.sellCoinPair(coinPair, amount))

def reportCurrentPrice(args):
	coinA, coinB = args.coinpair.split("/")
	keyDict = processConfiguration(args.keys)
	exchange = CCXTExchange(args.exchange, keyDict)

	try:
		priceInfo = exchange.getPriceInfoDict(coinA, coinB)
	except:
		print("Error Reporting Price!")

	buyPrice = priceInfo["ask"]
	sellPrice = priceInfo["bid"]
	midPrice = priceInfo["mid"]
	justifiedDifference = midPrice * exchange.getTransactionCost(coinA, coinB)

	print("BUY PRICE (Ask): {}\nSELL PRICE (Bid): {}\nJUSTIFIED DIFFERENCE: {}\n".format(buyPrice, sellPrice, justifiedDifference))


def main(argv):
	parser = argparse.ArgumentParser(description='Generate Price Information for Exchanges over 50 seconds at 5 second intervals')
	parser.add_argument('-e', '--exchange', required=True)
	parser.add_argument('-k', '--keys', required=True)
	subparsers = parser.add_subparsers(help='subcommands')

	summaryParser = subparsers.add_parser('report', help='summary help')
	summaryParser.add_argument('-c', '--coinpair', default=None)
	summaryParser.set_defaults(func=reportCurrentPrice)

	summaryParser = subparsers.add_parser('summary', help='summary help')
	summaryParser.add_argument('-c', '--coins', default=None)
	summaryParser.set_defaults(func=accountSummary)

	summaryParser = subparsers.add_parser('buy', help='summary help')
	summaryParser.add_argument('-c', '--coinpair', required=True)
	summaryParser.add_argument('-n', '--amount', required=True)
	summaryParser.set_defaults(func=buyCoin)

	summaryParser = subparsers.add_parser('sell', help='summary help')
	summaryParser.add_argument('-c', '--coinpair', required=True)
	summaryParser.add_argument('-n', '--amount', required=True)
	summaryParser.set_defaults(func=sellCoin)

	args = parser.parse_args()
	args.func(args)

if __name__ == '__main__':
	main(sys.argv)
