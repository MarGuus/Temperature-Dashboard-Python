 var records = db.youCollection.find();
 records.forEach(function(doc) {
 var dateStr = doc.date;
 if(typeof dateStr === "string")
 {
 var date = new Date(dateStr);

 db.youCollection.update({_id: doc._id}, {$set: {date: date}})
 }})