#!/bin/bash
rsync --exclude="venv" -e "ssh -p2222" --progress --verbose -r * unko@a.ahoj.club:/var/www/segedin/.
