# Backend for Online Store
## Nathan Vik


## Help:

### Start DB Service:
sudo service mongodb status
sudo service mongodb start
sudo service mongodb stop

### Delete All Orders
from terminal
mongo
show dbs
use onlinestore
show collections
db.order.remove({}) to remove all
