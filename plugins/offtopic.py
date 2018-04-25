from cloudbot import hook


@hook.command('offtopic')
def offtopic(text, nick, message):
    if not text:
        return
    if text.startswith('#'):
        hash_text = 'reddit-tennis-' + text
    else:
        hash_text = '#reddit-tennis-' + text
    message('Please keep off-topic chat to a minimum, or take it to ' + hash_text)
