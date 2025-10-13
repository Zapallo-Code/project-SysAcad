#!/bin/bash
VAR_CONTEXT=$1

if [ "$VAR_CONTEXT" = "production" ]
then
    VAR_CONTEXT=production
else
    VAR_CONTEXT=development
fi
echo "environment set to: $VAR_CONTEXT"
export FLASK_CONTEXT=$VAR_CONTEXT
python3 app.py
