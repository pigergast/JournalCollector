# get all identified email address from ISSN and YEAR

import time
from pymed import PubMed

print(time.asctime(time.localtime(time.time())))

year1="2019"
year2="2021"
ISSN="1527-6546"

ISSNList = ["0020-7489", "1474-5151", "1074-8407", "0730-7659", "1445-8330", "0260-6917",
"0966-0429", "0029-6554", "0309-2402", "1527-6546", "1871-5192", "0964-3397", "0962-1067",
"1351-0126", "1545-102X", "0969-7330", "0020-8132", "1059-8405", "0162-220X", "1322-7696",
"1099-8004", "0961-5423", "2347-5625", "1462-3889", "1320-7881", "1876-1399", "1526-9523",
"1078-3903", "0029-6562", "0266-6138", "0197-4572", "1527-7941", "0283-9318", "1362-1017",
"0749-2081", "1472-6955", "1471-5953", "0897-1897", "0160-6891", "0002-936X", "0890-3344",
"0883-9417", "0031-5990", "0190-535X", "0882-5963", "1755-599X", "1748-3735", "8755-7223",
"1976-1317", "0889-4655", "0363-3624", "1054-7738", "1322-7114", "1538-2931", "0193-9459",
"1043-6596", "1748-2623", "1524-9042", "1522-2179", "1441-0745", "0099-1767", "0161-2840",
"0161-9268", "1037-6178", "2054-1058", "1071-5754", "0002-0443", "0148-4834", "0884-2175",
"0279-5442", "1682-3141", "0893-2190", "1043-4542", "0278-4807", "1057-3631", "1940-4921",
"1088-4602", "0737-1209", "1518-8345", "1742-7932", "0361-929X", "1055-3290", "0899-5885",
"1466-7681", "1539-0136", "0098-9134", "0888-0395", "0022-0124", "2047-3087", "0029-6465",
"1556-3693", "2327-6886", "0279-3695", "0080-6234", "0746-1739", "1089-9472", "0887-6274",
"1092-1095", "1078-7496", "0887-9311", "2005-3673", "1042-895X", "0737-0016", "1526-744X",
"0744-6020", "0894-3184", "1592-5986", "1555-4155", "1541-6577", "0001-2092", "0103-2100",
"1012-5302", "0813-0531", "1351-5578", "2377-9608", "2158-0782", "0361-1817", "1130-2399",
"1856-9528", "2287-2434", "2528-181X", "0210-5020", "2253-9832", "0898-0101", "1533-1458",
"1062-0303", "0743-2550", "2230-522X", "2155-8256", "2090-1429", "2322-1488", "2271-8362",
"1061-3749", "1744-9871", "0034-7167", "1557-3087", "1931-4485", "0730-4625", "2333-3936",
"0844-5621", "2380-9418", "1682-5055", "2345-5756", "1357-6321", "2169-9798", "1735-9066",
"1892-2678", "1073-6077", "1906-8107", "1878-1241", "1078-4535", "2039-439X", "0029-6473",
"1541-4612", "1897-3116"]

counter = 1
for ISSN in ISSNList:

  print(str(counter)+": "+ISSN)
  filename=str(counter)+"."+ISSN+"_"+year1+"-"+year2+".csv"

  pubmed = PubMed(tool="MyTool",email="tangkwo1@hotmail.com")
  query="((\""+year1+"/1/1\"[Date - Publication] : \""+year2+"/12/31\"[Date - Publication])) AND ("+ISSN+"[IS])"
  results = pubmed.query(query,max_results=9999)

  outfile = open(filename,"w",encoding="utf-8")

  for article in results:
#    print(article.pubmed_id,article.publication_date)
#    print(article.toJSON())

    for author in article.authors:
        aff = str(author.get("affiliation","NONE!"))
#        print(str(author.get("lastname","NONE!")) + "; " + str(author.get("firstname","NONE!")) + str(author.get("affiliation","NONE!")) + "\n")
        if aff.find("@") != -1:
            line = aff.split()
            for item in line:
                if item.find("@") != -1:
                    email = item
                    if email[-1] == ".":
                        email = email[0:-1]
            outfile.write(str(author.get("lastname","NONE!")) + "; " + str(author.get("firstname","NONE!")) + "; " + str(email) + "\n")

  outfile.close()
  counter = counter+1

print(time.asctime(time.localtime(time.time())))
