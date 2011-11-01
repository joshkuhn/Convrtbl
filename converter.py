import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

form = """<form action="/convert" method="post">
                <h2>Currency Converter</h2>
                <div>
                    <input type="text" name="quantity">
                    <select name="from">
                        <option selected>USD</option>
                        <option>Euro</option>
                        <option>Yuan</option>
                    </select> to                     
                    <select name="to">
                        <option>USD</option>
                        <option selected>Yuan</option>
                        <option>Euro</option>
                    </select>
                    <input type="submit" value="Convert" />
                </div>                
              </form>"""

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>'+ form + '</body></html>')


class Guestbook(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>')

        quantityIn = float(self.request.get('quantity'))
        fromCurrency = self.request.get('from')
        toCurrency = self.request.get('to')

        # only try the conversion if the user's input validates.
        if (validateInput(quantityIn, fromCurrency, toCurrency)):
            quantityOut = convert(quantityIn, fromCurrency, toCurrency)
            self.response.out.write(form + '<br>')
    
            self.response.out.write('<h3>' + str(quantityIn) + ' ' + fromCurrency)
            self.response.out.write(' is approximately ' + str(quantityOut) + ' ' + toCurrency)
        else:
            self.response.out.write('Ha!  Your plans have been foiled l33t h4x0r.');       

        self.response.out.write('</body></html>')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/convert', Guestbook)],
                                     debug=True)

def validateInput(quantity, fromCurrency, toCurrency):
    """
    This function checks types and ranges to avoid invalid input
    """
    supportedCurs = ['Euro', 'USD', 'Yuan']
    if fromCurrency not in supportedCurs:
        return False
    if toCurrency not in supportedCurs:
        return False
    if quantity is None:
        return False

    return True

def convert(quantity, fromCurrency, toCurrency):
    """ 
    all currencies are converted to the base currency (USD) first
    then to the target currency.  For this reason, our lookup table
    only needs conversions from 1 USD.
    """
        
    extab = {
    'Euro': 0.714,
    'Yuan': 6.35,
    'USD': 1
    }
    
    baseValue = quantity * extab[fromCurrency]
    finalValue = baseValue * extab[toCurrency]
        
    return finalValue

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
