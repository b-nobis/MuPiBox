#!/bin/bash
#

#https://raw.githubusercontent.com/splitti/MuPiBox/main
#SRC="https://mupibox.de/version/latest"
CONFIG="/etc/mupibox/mupiboxconfig.json"

# 1.0.8
/usr/bin/cat <<< $(/usr/bin/jq 'del(.mupibox.googlettslanguages)' ${CONFIG}) > ${CONFIG}
/usr/bin/cat <<< $(/usr/bin/jq 'del(.mupibox.mediaCheckTimer)' ${CONFIG}) > ${CONFIG}
/usr/bin/cat <<< $(/usr/bin/jq 'del(.mupibox.AudioDevices)' ${CONFIG}) > ${CONFIG}

# 1.0.8
/usr/bin/cat <<< $(/usr/bin/jq '.mupibox.googlettslanguages += [{"iso639-1": "ar", "Language": "Arabic"},{"iso639-1": "zh", "Language": "Chinese"},{"iso639-1": "cs","Language": "Czech"},{"iso639-1": "da","Language": "Danish"},{"iso639-1": "nl","Language": "Dutch"},{"iso639-1": "en","Language": "English"},{"iso639-1": "fi","Language": "Finnish"},{"iso639-1": "fr","Language": "French"},{"iso639-1": "de","Language": "German"},{"iso639-1": "el","Language": "Greek"},{"iso639-1": "hi","Language": "Hindi"},{"iso639-1": "it","Language": "Italian"},{"iso639-1": "ja","Language": "Japanese"},{"iso639-1": "no","Language": "Norwegian"},{"iso639-1": "pl","Language": "Polish"},{"iso639-1": "pt","Language": "Portuguese"},{"iso639-1": "ru","Language": "Russian"},{"iso639-1": "es","Language": "Spanish, Castilian"},{"iso639-1": "sv","Language": "Swedish"},{"iso639-1": "tr","Language": "Turkish"},{"iso639-1": "uk","Language": "Ukrainian"}]' ${CONFIG}) >  ${CONFIG}

# 1.0.8
DEVICE=$(/usr/bin/jq -r .spotify.physicalDevice ${CONFIG})
if [ "$DEVICE" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "hifiberry-dac" '.mupibox.physicalDevice = $v' ${CONFIG}) >  ${CONFIG}
fi

# 1.0.8
MAXVOL=$(/usr/bin/jq -r .mupibox.maxVolume ${CONFIG})
if [ "$MAXVOL" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "100" '.mupibox.maxVolume = $v' ${CONFIG}) >  ${CONFIG}
fi

# 2.0.0
XMAS=$(/usr/bin/cat ${CONFIG} | grep xmas)
if [[ -z ${XMAS} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "xmas" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
IMAN=$(/usr/bin/cat ${CONFIG} | grep ironman)
if [[ -z ${IMAN} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "ironman" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
CAP=$(/usr/bin/cat ${CONFIG} | grep captainamerica)
if [[ -z ${CAP} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "captainamerica" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
WOOD=$(/usr/bin/cat ${CONFIG} | grep wood)
if [[ -z ${WOOD} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "wood" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
MATRIX=$(/usr/bin/cat ${CONFIG} | grep matrix)
if [[ -z ${MATRIX} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "matrix" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
MINT=$(/usr/bin/cat ${CONFIG} | grep mint)
if [[ -z ${MINT} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "mint" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
DANGER=$(/usr/bin/cat ${CONFIG} | grep danger)
if [[ -z ${DANGER} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "danger" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi
CINEMA=$(/usr/bin/cat ${CONFIG} | grep cinema)
if [[ -z ${CINEMA} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "cinema" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi

#2.1.0
LEDMAX=$(/usr/bin/jq -r .shim.ledBrightnessMax ${CONFIG})
if [ "$LEDMAX" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "100" '.shim.ledBrightnessMax = $v' ${CONFIG}) >  ${CONFIG}
fi

LEDMIN=$(/usr/bin/jq -r .shim.ledBrightnessMin ${CONFIG})
if [ "$LEDMIN" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "10" '.shim.ledBrightnessMin = $v' ${CONFIG}) >  ${CONFIG}
fi

#3.0.0
PM2RAMLOG=$(/usr/bin/jq -r .pm2.ramlog ${CONFIG})
if [ "$PM2RAMLOG" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "0" '.pm2.ramlog = $v' ${CONFIG}) >  ${CONFIG}
fi

EARTH=$(/usr/bin/cat ${CONFIG} | grep earth)
if [[ -z ${EARTH} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "earth" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi

STEAMPUNK=$(/usr/bin/cat ${CONFIG} | grep steampunk)
if [[ -z ${STEAMPUNK} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "steampunk" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi

FANTASY_BUTTERFLIES=$(/usr/bin/cat ${CONFIG} | grep fantasybutterflies)
if [[ -z ${FANTASY_BUTTERFLIES} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "fantasybutterflies" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi

LINES=$(/usr/bin/cat ${CONFIG} | grep lines)
if [[ -z ${LINES} ]]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "lines" '.mupibox.installedThemes? += [$v]' ${CONFIG}) >  ${CONFIG}
fi

#3.0.2
TELEGRAM=$(/usr/bin/cat ${CONFIG} | grep telegram)
if [[ -z ${TELEGRAM} ]]; then
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.telegram.token = $v' ${CONFIG}) >  ${CONFIG}
	/usr/bin/cat <<< $(/usr/bin/jq '.telegram.active = false' ${CONFIG}) >  ${CONFIG}
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.telegram.chatId = $v' ${CONFIG}) >  ${CONFIG}                 
fi

#3.0.2
WLED=$(/usr/bin/cat ${CONFIG} | grep wled)
if [[ -z ${WLED} ]]; then
	/usr/bin/cat <<< $(/usr/bin/jq '.wled.active = false' ${CONFIG}) >  ${CONFIG}
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.wled.startup_id = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.wled.main_id = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.wled.shutdown_id = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "255" '.wled.brightness_default = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "128" '.wled.brightness_dimmed = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "true" '.wled.boot_active = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "true" '.wled.shutdown_active = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "115200" '.wled.baud_rate = $v' ${CONFIG}) >  ${CONFIG}
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "/dev/ttyUSB0" '.wled.com_port = $v' ${CONFIG}) >  ${CONFIG}
fi

#3.2.6
IPCONTROL=$(/usr/bin/cat ${CONFIG} | grep ip_control_backend)
if [[ -z ${IPCONTROL} ]]; then
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "false" '.mupibox.ip_control_backend = $v' ${CONFIG}) >  ${CONFIG}
fi
/usr/bin/cat <<< $(/usr/bin/jq 'del(.wled.ip)' ${CONFIG}) > ${CONFIG}
WLED=$(/usr/bin/cat ${CONFIG} | grep com_port)
if [[ -z ${WLED} ]]; then
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "" '.wled.startup_id = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "255" '.wled.brightness_default = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "128" '.wled.brightness_dimmed = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "true" '.wled.boot_active = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "true" '.wled.shutdown_active = $v' ${CONFIG}) >  ${CONFIG}                 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "115200" '.wled.baud_rate = $v' ${CONFIG}) >  ${CONFIG}
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "/dev/ttyUSB0" '.wled.com_port = $v' ${CONFIG}) >  ${CONFIG}
	
fi

#3.3.4
GPU=$(/usr/bin/jq -r .chromium.gpu ${CONFIG})
if [ "$GPU" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "false" '.chromium.gpu = $v' ${CONFIG}) >  ${CONFIG}
fi
SCROLLANI=$(/usr/bin/jq -r .chromium.sccrollanimation ${CONFIG})
if [ "$SCROLLANI" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "false" '.chromium.sccrollanimation = $v' ${CONFIG}) >  ${CONFIG}
fi
CACHEPATH=$(/usr/bin/jq -r .chromium.cachepath ${CONFIG})
if [ "$CACHEPATH" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "/home/dietpi/.mupibox/chromium_cache" '.chromium.cachepath = $v' ${CONFIG}) >  ${CONFIG}
fi
CACHESIZE=$(/usr/bin/jq -r .chromium.cachesize ${CONFIG})
if [ "$SCROLLANI" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "32" '.chromium.cachesize = $v' ${CONFIG}) >  ${CONFIG}
fi
KIOSKMODE=$(/usr/bin/jq -r .chromium.kiosk ${CONFIG})
if [ "$SCROLLANI" == "null" ]; then 
	/usr/bin/cat <<< $(/usr/bin/jq --arg v "true" '.chromium.kiosk = $v' ${CONFIG}) >  ${CONFIG}
fi

/usr/bin/cat <<< $(/usr/bin/jq '.mupibox.AudioDevices += [{"tname": "mupihat","ufname": "MuPiHat for MuPiBox"},{"tname": "rpi-bcm2835-3.5mm","ufname": "Onboard 3.5mm output"},{"tname": "rpi-bcm2835-hdmi","ufname": "Onboard HDMI output"},{"tname": "hifiberry-amp","ufname": "HifiBerry AMP / AMP+"},{"tname": "hifiberry-dac","ufname": "HifiBerry DAC / MiniAmp"},{"tname": "hifiberry-dacplus","ufname": "HifiBerry DAC+ / DAC+ Pro / AMP2"},{"tname": "usb-dac","ufname": "Any USB Audio DAC (Auto detection)"}]' ${CONFIG}) >  ${CONFIG}
