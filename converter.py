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
                        <option>Rupee</option>
                        <option>Yuan</option>
                        <option>Yen</option>                        
                    </select> to                     
                    <select name="to">
                        <option>USD</option>
                        <option>Euro</option>
                        <option>Rupee</option>
                        <option selected>Yuan</option>
                        <option>Yen</option>
                    </select>
                    <input type="submit" value="Convert" />
                </div>                
              </form>"""

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>'+ form + '</body></html>')


class Converter(webapp.RequestHandler):    
    extab = {
        'Euro': 0.714,
        'Yuan': 6.35,
        'Yen': 75.89,
        'Rupee': 49.5,
        'USD': 1
    }

    def validateInput(self, quantity, fromCurrency, toCurrency):
        """
        This function checks types and ranges to avoid invalid input
        """
        if not self.extab.has_key(fromCurrency):
            return False
        if not self.extab.has_key(toCurrency):
            return False
        if quantity is None:
            return False
        try:
            float(quantity)
        except:
            # could not parse a float out of the quantity string.
            return False

        return True

    def convert(self, quantity, fromCurrency, toCurrency):
        """ 
        all currencies are converted to the base currency (USD) first
        then to the target currency.  For this reason, our lookup table
        only needs conversions from 1 USD.
        """
        
        baseValue = quantity / self.extab[fromCurrency]
        finalValue = baseValue * self.extab[toCurrency]
            
        return finalValue

    def post(self):
        self.response.out.write('<html><body>')

        quantityIn = self.request.get('quantity')
        fromCurrency = self.request.get('from')
        toCurrency = self.request.get('to')

        # only try the conversion if the user's input validates.
        if (self.validateInput(quantityIn, fromCurrency, toCurrency)):
            quantityOut = self.convert(float(quantityIn), fromCurrency, toCurrency)
            self.response.out.write(form + '<br>')
    
            self.response.out.write('<h3>' + str(quantityIn) + ' ' + fromCurrency)
            self.response.out.write(' is approximately ' + str(quantityOut) + ' ' + toCurrency + '</h3>')
        else:
            self.response.out.write(form + '<br>')
            self.response.out.write('<h3>Invalid input, please try again.</h3>');       

        self.response.out.write('</body></html>')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/convert', Converter)],
                                     debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
