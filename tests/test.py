import argparse
from unittest import mock




@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(token='token', chats=['12345']))
def test_subprocess(mock_args):
    from src.script import Subprocess
    from src.script import bot

    def mock_sending(chat_id, output):
        assert chat_id == 'unique_id'
        assert output == 'Hello World!\n'
        exit()

    bot.send_message = mock_sending

    subprocess = Subprocess('unique_id')
    subprocess.add_symbols('echo "Hello World!"\n')




if __name__ == '__main__':
    test_subprocess()
