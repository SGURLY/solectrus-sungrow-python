## solectrus-sungrow-python v0.01
###Pls Note that this is NOT officially approved by solecturs devs - and defentily more of a hacky solution rather than production ready

This is using a [sungrow python wrapper](https://github.com/wallento/sungrow-websocket) and [Solectrus](https://github.com/solectrus).
Pls make sure to go and check out these repos!

## Usage (only tested on raspi4)
### Solectrus

1. For Installation of Solectrus pls follow the [steps mentioned in the solectrus repo](https://github.com/solectrus/hosting)
2. **Before** you run `docker compose up` finish below steps

### Sungrow Importer

1. Copy these files in the previously installed solectrus folder
2. Edit the previously downloaded `.env` file and append the line `SUNGROW_IP_ADDR=<YOUR IP ADDR>`
3. Append the content from this `docker-compose.yml` (Line 4 and following) to the solectrus one
4. Run `docker compose up` and have fun!
 


