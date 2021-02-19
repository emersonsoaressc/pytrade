import pandas as pd 
import MetaTrader5 as mt5 
import time
import functions as fc 


def extrair_base(ativos, timeframe, n=500):
    data = pd.DataFrame()
    if not mt5.initialize():
        print('Inicialização falhou! error code =', mt5.last_error())
        quit()
    else:
        print('Inicialização concluida!')
    # se o símbolo não estiver disponível no MarketWatch, fazemos a adição
    for i in ativos:
        symbol_info = mt5.symbol_info(i)
        if symbol_info is None:
            print(i, "não encontrado, o robô não pode prosseguir")
            mt5.shutdown()
            quit()
        if not symbol_info.visible:
            print(i, "não está visível, tentando ligar...")
            if not mt5.symbol_select(i,True):
                print("O ticker selecionado ({}}) falhou, fechando...",i)
                mt5.shutdown()
                quit()
    for i in ativos:
        tf = bool(f'mt5.TIMEFRAME_{timeframe}') 
        df = mt5.copy_rates_from_pos(i, tf, 0 ,n)
        df = pd.DataFrame(df)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[['time','close']].set_index('time')
        df = df.rename(columns={'close':f'{i}'})
        data = pd.concat([df, data], axis = 1)
    return data


def trade(action,ativo,qtd):
    if not mt5.initialize():
        print('Inicialização falhou! error code =', mt5.last_error())
        quit()
    else:
        print('Inicialização concluida!')
    # se o símbolo não estiver disponível no MarketWatch, adicionamo-lo
    symbol_info = mt5.symbol_info(ativo)
    if symbol_info is None:
        print(ativo, "não encontrado, o robô não pode prosseguir")
        mt5.shutdown()
        quit()
    if not symbol_info.visible:
        print(ativo, "não está visível, tentando ligar...")
        if not mt5.symbol_select(ativo,True):
            print("O ticker selecionado ({}}) falhou, fechando...",ativo)
            mt5.shutdown()
            quit()
    symbol = ativo
    
    if action == 'compra':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask       
    elif action == 'venda':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    lot = float(qtd)
    point = mt5.symbol_info(symbol).point
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type, 
        "price": price,
        #"sl": price - 100 * point,
        #"tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    } 
    # enviamos a solicitação de negociação
    result = mt5.order_send(request)
    # verificamos o resultado da execução
    print("Ordem ENVIADA! : Foi efetuada uma {} de {} de {} a {} com desvio de {} pontos".format(action,lot,symbol,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Ordem falhou, retcode={}".format(result.retcode))
        # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        


def total_ordens():
    # estabelecemos a conexão ao MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    time.sleep(2)
    positions_total=mt5.positions_total()
    if positions_total>0:
        print("Total positions=",positions_total)
    else:
        print("Positions not found")
    return positions_total

