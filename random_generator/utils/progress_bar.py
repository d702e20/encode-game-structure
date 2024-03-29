import sys


def progress_bar(current, max):
    """Speaks for itself. Its a progressbar"""
    if current == max:
        print('     *Complete*      ')
        return
    percentage = int(current / max * 100)
    print(f'Progress: {current}, {percentage}%')
    sys.stdout.write("\033[F")  # Cursor up one line
