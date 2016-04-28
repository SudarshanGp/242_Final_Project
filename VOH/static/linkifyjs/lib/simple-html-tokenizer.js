'use strict';

exports.__esModule = true;

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _simpleHtmlTokenizerHtml5NamedCharRefs = require('./simple-html-tokenizer/html5-named-char-refs');

var _simpleHtmlTokenizerHtml5NamedCharRefs2 = _interopRequireDefault(_simpleHtmlTokenizerHtml5NamedCharRefs);

var _simpleHtmlTokenizerEntityParser = require('./simple-html-tokenizer/entity-parser');

var _simpleHtmlTokenizerEntityParser2 = _interopRequireDefault(_simpleHtmlTokenizerEntityParser);

var _simpleHtmlTokenizerEventedTokenizer = require('./simple-html-tokenizer/evented-tokenizer');

var _simpleHtmlTokenizerEventedTokenizer2 = _interopRequireDefault(_simpleHtmlTokenizerEventedTokenizer);

var _simpleHtmlTokenizerTokenizer = require('./simple-html-tokenizer/tokenizer');

var _simpleHtmlTokenizerTokenizer2 = _interopRequireDefault(_simpleHtmlTokenizerTokenizer);

var _simpleHtmlTokenizerTokenize = require('./simple-html-tokenizer/tokenize');

var _simpleHtmlTokenizerTokenize2 = _interopRequireDefault(_simpleHtmlTokenizerTokenize);

var HTML5Tokenizer = {
	HTML5NamedCharRefs: _simpleHtmlTokenizerHtml5NamedCharRefs2['default'],
	EntityParser: _simpleHtmlTokenizerEntityParser2['default'],
	EventedTokenizer: _simpleHtmlTokenizerEventedTokenizer2['default'],
	Tokenizer: _simpleHtmlTokenizerTokenizer2['default'],
	tokenize: _simpleHtmlTokenizerTokenize2['default']
};

exports['default'] = HTML5Tokenizer;
module.exports = exports['default'];