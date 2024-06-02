from coinpayments import CoinPaymentsAsyncIO
from config import (
    COINPAYMENTS_PUBLIC_KEY,
    COINPAYMENTS_PRIVATE_KEY,
    COINS
)
import asyncio



coinp = CoinPaymentsAsyncIO(
    public_key=COINPAYMENTS_PUBLIC_KEY,
    private_key=COINPAYMENTS_PRIVATE_KEY
)




async def get_balances():

    result = await coinp.coinpayments(
        data={
            'cmd': 'balances'
        },
        method='POST'
    )

    if result['error'] != 'ok':
        raise Exception(
            f'The api returned an error when retrieving account balance => {result}'
            )
    

    return result['result']



async def send_mass_withdrawal_request(mass_withdrawal_data: list):    

    result_send = await coinp.coinpayments(
        data={
            'cmd': 'create_mass_withdrawal',
            'wd': mass_withdrawal_data
        },
        method='POST'
    )

    return result_send



async def main():


    balances: dict = await get_balances()

    mass_withdrawal_data = []

    for coin, coin_data in COINS.items():

        balance_data: dict = balances.get(coin, None)

        if balance_data is None or not balance_data['balance']:
            print(f'No balance found for currency `{coin}` (Withdrawal for this currency will be ignored).')
            continue


        address = coin_data['address']
        dest_tag = coin_data['dest_tag']
        amount = float(coin_data['amount']) or float(balance_data['balancef'])

        data = {
            'cmd': 'create_withdrawal',
            'currency': coin,
            'amount': amount,
            'address': address,
            'auto_confirm': 1
        }

        if dest_tag:
            data['dest_tag'] = dest_tag

        mass_withdrawal_data.append(data)


    if mass_withdrawal_data:
        result = await send_mass_withdrawal_request(
            mass_withdrawal_data=mass_withdrawal_data
            )

        print(' [Result] '.center(100, '-'))
        print(result)
    else:
        print('There are no coins to withdraw.')



if __name__ == "__main__":
    asyncio.run(main())

