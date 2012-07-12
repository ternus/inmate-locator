import mechanize, re, BeautifulSoup, string

class Inmate:
    firstName = ""
    lastName = ""
    inmateId = ""
    status = False
    location = ""
    releaseDate = ""
    lastUpdate = ""
    
    def __unicode__(self):
        return "#" + self.inmateId + ": " + self.firstName + " " + self.lastName + " Active: " + str(self.status) + " Location: " + self.location + " Release Date: " + self.releaseDate

    def __str__(self):
        return self.__unicode__()
    def __repr__(self):
        return str(self)


def encode_inmate(inmate):
    return inmate.__dict__


siteIds = {
    "AL" : None,
    "AK" : "2001",
    "AR" : "4999",
    "AZ" : None,
    "CA" : None,
    "CO" : None,
    "CT" : None,
    "DE" : "8000",
    "FL" : "10000",
    "GA" : None,
    "HI" : "50000",
    "IA" : "16000",
    "ID" : "13000",
    "IL" : "14004",
    "IN" : None,
    "KS" : None,
    "KY" : "18000",
    "LA" : "19000",
    "MA" : None,
    "MD" : "21999",
    "ME" : None,
    "MI" : "25000",
    "MN" : "24002",
    "MO" : "26000",
    "MS" : "23005",
    "MT" : None,
    "NC" : "34003",
    "ND" : "35000",
    "NE" : "28000",
    "NH" : None,
    "NJ" : "31000",
    "NM" : None,
    "NV" : None,
    "NY" : "33004",
    "OH" : "36001",
    "OK" : "37000",
    "OR" : "38000",
    "PA" : "39000",
    "RI" : "40900",
    "SC" : "41000",   
    "SD" : None,
    "TN" : None,
    "TX" : None,
    "UT" : "45000",
    "VA" : "47000",
    "VT" : "46000",
    "WA" : "48626",
    "WV" : None,
    "WI" : "50001",
    "WY" : "51000",
    "PR" : "53000",
    }


def vinelink(inmateId, state):
    
    if not state in siteIds or siteIds[state] is None:
        return "Error: State not supported, sorry."

    br = mechanize.Browser()
    br.open("https://www.vinelink.com/vinelink/siteInfoAction.do?siteId=%s" % siteIds[state])
    assert br.viewing_html()
    print br.title()
    br.follow_link(url_regex = re.compile("initSearchForm"))
    print br.title()
    br.select_form("searchForm")

    br["id"] = inmateId
    response = br.submit()
    rtext = response.read()
    print rtext

    s = BeautifulSoup.BeautifulSoup(rtext).findChild("tbody").prettify()
    b = BeautifulSoup.BeautifulSoup(s)
    res = map(string.strip, filter(lambda x: x != u'\n', b.findChildren("td", text=True)))
    print res


# John Smith: 219399
def ALsearch(inmateId=None,firstName="",lastName=""):
    br = mechanize.Browser()
    response = br.open("http://www.doc.state.al.us/inmresults.asp?AIS=%s&FirstName=%s&LastName=%s" % (inmateId, firstName, lastName))
    rtext = response.read()

    s = BeautifulSoup.BeautifulSoup(rtext)
    return s

def getTds(s):
    return filter(lambda x: x, map(string.strip, s.findAll("td", text=True)))

# James Smith: 134202
def AZsearch(inmateId):
    br = mechanize.Browser()
    theurl = "http://www.azcorrections.gov/inmate_datasearch/results_Minh.aspx?InmateNumber=%s" % (inmateId)
    response = br.open(theurl)
    rtext = response.read()

    # Fix AZ DOC's broken HTML.
    s = BeautifulSoup.BeautifulSoup(re.sub("\"\" class", "\" class", rtext))
    guy = Inmate()
    guy.inmateId = inmateId

    sv = s.find(id="ctl00_CentralContent_GridView1")
    if not sv:
        return None

    bv = s.find(id="ctl00_CentralContent_GridView1")
    guy.firstName = getTds(bv)[5]
    guy.lastName = getTds(bv)[4]

    bv = s.find(id="ctl00_CentralContent_GridView4")
    guy.releaseDate = getTds(bv)[-1]

    bv = s.find(id="ctl00_CentralContent_GridView5")
    guy.location = getTds(bv)[-2]

    sv = s.find(id="ctl00_CentralContent_GridView6")
    if getTds(sv)[-1] == "ACTIVE":
        guy.status = True
    else:
        guy.status = False
    guy.realStatus = getTds(sv)[-1]
    guy.lastUpdate = getTds(sv)[-3]
    guy.url = theurl

    return guy
