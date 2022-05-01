#!/bin/bash

# 制御ボタン番号と照明制御時の制御名とのマッピング
function mapping_light(){
    # ========================================
    # 操作ボタン番号（device_number）と
    # 制御名（control_name）の対応を記載
    # ========================================
    # device_number control_name
    echo 0 on          # light on
    echo 1 off         # light off
    echo 2 night_light # night light
    echo 3 up          # brightness up
    echo 4 down        # brightness down
    echo 5 all_light   # all light
}

function mapping_air_conditioner(){
    echo 0 cooler_on
    echo 1 heater_on
    echo 2 power_off
    echo 3 dry_on
}

function mapping_electric_fan(){
    echo 2 power_off
    echo 0 power_on
    echo 1 fan_up
}

# ============
# main routine
# ============
exe_func=""
exe_flag=0

case "$1" in
    light )
        exe_func=mapping_light
        exe_flag=1
        shift
        ;;

    air )
        exe_func=mapping_air_conditioner
        exe_flag=1
        shift
        ;;

    fan )
        exe_func=mapping_electric_fan
        exe_flag=1
        shift
        ;;

    * )
        shift
        ;;
esac

if [ ${exe_flag} -eq 1 ]; then
    # ==================
    # 出力対象の情報取得
    # ==================
    {
        echo  import sys
        echo  import json
        echo "sys.path.append('..')"
        echo  from adrsirlib import Adrsir
        echo "model = Adrsir()"
        echo "info = {}"
        ${exe_func} | while read device_number control_name; do
        echo "info['${control_name}'] = model.get(${device_number})"
        done
        echo "data = json.dumps(info, indent=4)"
        echo "print(data)"
    } | python3
fi
