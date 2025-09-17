#!/bin/bash
./setup-env.sh
./start-backend.sh &
sleep 2
./start-frontend.sh