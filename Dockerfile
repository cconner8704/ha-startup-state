FROM python:3
MAINTAINER Chris Conner chrism.conner@gmail.com
# Had issues with lights turning off randomly because of some smartthings/mqtt-bridge bug
# Had to implement PhilRW fix in https://github.com/stjohnjohnson/smartthings-mqtt-bridge/issues/113
# However, state was lost of reboot, this is my fix.

# Add script
ADD dockerStart.sh /dockerStart.sh
ADD set-ha-state.py /

# Expose Configuration Volume
VOLUME /config

# Set config directory
ENV CONFIG_DIR=/config
ENV MQTT_BRIDGE_SERVER=localhost
ENV MQTT_BRIDGE_PORT=8080

# Entry point to make ENV vars work in CMD
ENTRYPOINT ["/dockerStart.sh"]

# Install keyring
RUN pip install keyring


# Run the service
CMD [ "python", "/set-ha-state.py", "${MQTT_BRIDGE_SERVER}:${MQTT_BRIDGE_PORT}", "${CONFIG_DIR}/state.json" ]
