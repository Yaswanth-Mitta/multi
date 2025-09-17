#!/bin/bash
source .env
export PUBLIC_IP
envsubst < frontend-nextjs/.env.local > frontend-nextjs/.env.local.tmp
mv frontend-nextjs/.env.local.tmp frontend-nextjs/.env.local