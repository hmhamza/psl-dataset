import json


def print_vocab_info():
    config = json.load(open('../configs/vocab.json'))
    
    total_words = 0
    for category in config['vocabulary']:
        print(category['category']+': '+str(len(category['words'])))
        total_words += len(category['words'])

    print('\nTotal categories: '+str(len(config['vocabulary'])))
    print('Total words: '+str(total_words))
            
            
print_vocab_info()