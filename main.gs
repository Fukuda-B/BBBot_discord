// Google App Script
// TranslateText
// Request: URI?text='BBB'&source='en'&target='ja'
function doGet(e) {
  var p = e.parameter, translatedText = LanguageApp.translate(p.text, p.source, p.target), body;
  if (translatedText) {
    body = {
      res: translatedText
    };
  } else {
    body = {
      res: 'Error'
    }    
  }
  var response = ContentService.createTextOutput();
  response.setMimeType(ContentService.MimeType.JSON);
  response.setContent(JSON.stringify(body));
  return response;
}