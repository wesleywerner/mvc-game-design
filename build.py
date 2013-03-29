#!/usr/bin/env python
import os
import sys
import shutil

TOC_INCLUDE='# Table of contents\n\n[TOC]\n\n'
STYLE_INCLUDE='<link rel="stylesheet" type="text/css" href="res/style.css">'
BUILD_FILENAME='MVC Game Design by Wesley.html'

if __name__ == '__main__':
    print('checking dependencies...')
    try:
        import markdown
    except Exception as e:
        print(e)
        print('failed to load markdown.\nPlease install it, usually named "python-markdown" in your package manager')
        sys.exit(1)
    try:
        import pygments
    except Exception as e:
        print(e)
        print('syntax highlighting requires pygments installed. usually named "python-pygments" in your package manager, or see http://pygments.org')
        sys.exit(1)

    print('building documentation...')
    with open('README.md', 'r') as intext:
        rawtext = TOC_INCLUDE + ''.join(intext.readlines())
        html = markdown.markdown(
                    rawtext, extensions=[
                                        'toc', 
                                        'fenced_code',
                                        'codehilite(guess_lang=False)'
                        ]
                    )
    with open(BUILD_FILENAME, 'w') as outtext:
        outtext.write(STYLE_INCLUDE)
        outtext.write(html)
    print('wrote file "%s"' % (BUILD_FILENAME,))
