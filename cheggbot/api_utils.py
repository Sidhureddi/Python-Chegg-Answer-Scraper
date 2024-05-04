import requests
from bs4 import BeautifulSoup
import json
import unicodedata
import numpy as np
import random
import pandas as pd



def process_question(qid,headers):

	'''json_data = {
		'operationName': 'QnaPageQuestionByLegacyId',
		'variables': {
			'id': int(qid),
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '26efed323ef07d1759f67adadd2832ac85d7046b7eca681fe224d7824bab0928',
			},
		},
	}
	response = requests.post('https://gateway.chegg.com/one-graph/graphql',headers=headers, json=json_data)
	try:
		question_raw = json.loads(response.content)
		question = question_raw['data']['questionByLegacyId']['content']['body']
		return question
	except:
		print(response.content)
		return 'QUESTION_FETCH_FAILED'''
	
	return ''
		



def find_text(dictionary, target_key, path=None, parent=None, grouped_list=None):
	
	if path is None:
		path = []

	results = []
	
	if grouped_list is None:
		grouped_list = {}
	
	
	result = {}
	
	for key, value in dictionary.items():
		
		new_path = path + [key]
		
		if key == target_key:
			
			
			second_path = path[1]
			
			if second_path not in grouped_list:
				grouped_list[second_path] = []
				#print(second_path, 'available')
			grouped_list[second_path].append({'text':value,'type':parent['type']})
			

		if isinstance(value, dict):
			results.extend(find_text(value, target_key, new_path, dictionary,grouped_list))
			
		elif isinstance(value, list):
			for idx, item in enumerate(value):
				if isinstance(item, dict):
					item_path = new_path + [idx]  # Include the list index in the path
					results.extend(find_text(item, target_key, item_path, dictionary,grouped_list))
	
	return grouped_list




def identify_answer_type(qid,headers):
	
	json_data = {
		'operationName': 'NonSubQnaPageAnswerCount',
		'variables': {
			'id': int(qid),
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '800fef75be646692f255fab8d983df6faf364b207335da33afef1ce4866ed6d4',
			},
		},
	}

	response = requests.post('https://gateway.chegg.com/one-graph/graphql', headers=headers, json=json_data)
	try:
		data = json.loads(response.content)
		answer_type_available = data['data']['questionByLegacyId']['displayAnswers']
		return answer_type_available
	except:
		print(response.content)
		return 'ANSWER_TYPE_FAILED'


def process_ai_TextAnswer(jfile,COOKIE,headers,question,webhook_script,completeName):
	
	
	print('[*] Answer type : SBS Answer')
	
	question = BeautifulSoup(question, 'html.parser')
	for img in question.findAll('img'):
		if img.get('src').startswith("//"):
			print(img)
			img['src'] = img['src'].replace('//', 'https://')
			try:
				img['style'] =  img['style'].replace('height', 'h')
			except:
				pass
			print(img['src'])

	question = str(question)
	legacy_id = jfile['data']['questionByLegacyId']['displayAnswers']['id']
	answer = jfile['data']['questionByLegacyId']['displayAnswers']['bodyMdText']
	html = '''<html>
	<head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width">
	  <title>MathJax example</title>
	 <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>
	<style>pre.code {
	  white-space: pre-wrap;
		background-color:#ededed;
	display: inline-block;
	width: 65em;
		padding-left: auto; /* now works */
	  margin-left: 10;  /* now works */

	}
	pre.code::before {
	  counter-reset: listing;

	}
	pre.code code {
	  counter-increment: listing;
	}
	pre.code code::before {
	  content: counter(listing) " ";
	  display: inline-block;
	  width: 2em;         /* now works */
	  padding-left: auto; /* now works */
	  margin-left: auto;  /* now works */
	  text-align: right;  /* now works */
		background-color:#d9d7d7;
	color:red;
	}
	</style>
	<style>p {
	  font-family: "Leelawadee UI";
	}</style>
	<style>
	.steps {
		width: 100%;
		background-color: rgb(239, 245, 254);
		line-height: 1;
		font-size: 0.875rem;
		font-weight: bold;
		padding: 0.75rem 1rem;
		border: 1px solid rgb(231, 231, 231);
		box-sizing: border-box;
		display: flex;
		-webkit-box-pack: justify;
		justify-content: space-between;
		cursor: pointer;
	}
	</style>
	</head>
	<body>'''

	
	review_data = {
		'operationName': 'ReviewsV2',
		'variables': {
			'reviewForContentQueryArguments': {
				'contentId': str(legacy_id),
				'contentReviewType': 'LIKE_DISLIKE',
				'contentType': 'ANSWER',
			},
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1',
			},
		},
	}
	
	response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=COOKIE, headers=headers, json=review_data)
	review_data = json.loads(response.content)

	try:
		if review_data['data']['allReviews'][0]['contentReviewValue'] == 'LIKE':
			likes = review_data['data']['allReviews'][0]['count']
			try:
				if review_data['data']['allReviews'][1]['contentReviewValue'] == 'DISLIKE':
					dislikes = review_data['data']['allReviews'][1]['count']
				else:
					pass
			except:
				dislikes = 0
			
		elif review_data['data']['allReviews'][0]['contentReviewValue'] == 'DISLIKE':
			dislikes = review_data['data']['allReviews'][0]['count']
			likes = 0
	except:
		likes = 0
		dislikes = 0

	rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes ='+str(likes)+'</h3><h3 style="background-color:powderblue;">Dislikes ='+str(dislikes)+'</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'
	answer = answer.replace('\n','<br>')							

	with open(completeName,'w', encoding='UTF-8') as e:
		e.write(html)
		e.write(rating)
		e.write('<head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>')
		e.write('<div class="container">'+str(question)+'</div>')
		e.write('<div class="container">'+answer+'</div>')
		e.write(webhook_script)
		e.close()
	



def process_ai_sbs(jfile,COOKIE,headers,question,webhook_script,completeName):
	
	
	print('[*] Answer type : SBS Answer')
	
	question = BeautifulSoup(question, 'html.parser')
	for img in question.findAll('img'):
		if img.get('src').startswith("//"):
			print(img)
			img['src'] = img['src'].replace('//', 'https://')
			try:
				img['style'] =  img['style'].replace('height', 'h')
			except:
				pass
			print(img['src'])

	question = str(question)
	final_answer = '<p><strong>Final Answer</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['body']['correctAnswerMdText']+'</p>'
	legacy_id = jfile['data']['questionByLegacyId']['displayAnswers']['id']
	
	ans = []
	code_data_html = []
	number_of_steps = jfile['data']['questionByLegacyId']['displayAnswers']['body']['steps']
	for i in range(len(number_of_steps)):
		
		ans.append('<div class="steps">Step '+str(i+1)+' of '+str(len(number_of_steps))+'</div>')
		
		step = number_of_steps[i]['stepMdText']
		explanation = number_of_steps[i]['explanationMdText']
		
		
		if "\n" in step:
			cd_data = []
			ans.append('CODE_SNIPPET_PLACEHOLDER')
			code_data = step.split('\n')
			for c_data in code_data:
				codeData = '<code>'+str(c_data)+'</code>\n'
				cd_data.append(codeData)
			code_data_html.append(''.join(cd_data))
		else:
			ans.append(f'<p>{step}</p>')
		
		ans.append(f'<div class="explanation" style="margin-left:30px;"><p><b>Explanation</b></p><p>{explanation}</p></div>')
	
	stepByStep = ['<h3>Steps</h3>']
	for x in ans:
		stepByStep.append('<p>'+x+'</p>')
	loop = 0
	print(stepByStep)
	for i in range(len(stepByStep)):
		if stepByStep[i] == '<p>CODE_SNIPPET_PLACEHOLDER</p>':
			
			stepByStep[i] = '<pre class="code">'+code_data_html[loop]+'</pre>'
			loop+=1
			print(loop)
		else:
			pass
		
	
	answer = unicodedata.normalize("NFKD", str(''.join(stepByStep)))
	answer = answer.replace('$', '`')

	html = '''<html>
	<head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width">
	  <title>MathJax example</title>
	 <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>
	<style>pre.code {
	  white-space: pre-wrap;
		background-color:#ededed;
	display: inline-block;
	width: 65em;
		padding-left: auto; /* now works */
	  margin-left: 10;  /* now works */

	}
	pre.code::before {
	  counter-reset: listing;

	}
	pre.code code {
	  counter-increment: listing;
	}
	pre.code code::before {
	  content: counter(listing) " ";
	  display: inline-block;
	  width: 2em;         /* now works */
	  padding-left: auto; /* now works */
	  margin-left: auto;  /* now works */
	  text-align: right;  /* now works */
		background-color:#d9d7d7;
	color:red;
	}
	</style>
	<style>p {
	  font-family: "Leelawadee UI";
	}</style>
	<style>
	.steps {
		width: 100%;
		background-color: rgb(239, 245, 254);
		line-height: 1;
		font-size: 0.875rem;
		font-weight: bold;
		padding: 0.75rem 1rem;
		border: 1px solid rgb(231, 231, 231);
		box-sizing: border-box;
		display: flex;
		-webkit-box-pack: justify;
		justify-content: space-between;
		cursor: pointer;
	}
	</style>
	</head>
	<body>'''

	
	review_data  = {
		'operationName': 'ReviewsV2',
		'variables': {
			'reviewForContentQueryArguments': {
				'contentId': str(legacy_id),
				'contentReviewType': 'LIKE_DISLIKE',
				'contentType': 'ANSWER',
			},
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1',
			},
		},
	}
	response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=COOKIE, headers=headers, json=review_data)
	review_data = json.loads(response.content)

	try:
		if review_data['data']['allReviews'][0]['contentReviewValue'] == 'LIKE':
			likes = review_data['data']['allReviews'][0]['count']
			try:
				if review_data['data']['allReviews'][1]['contentReviewValue'] == 'DISLIKE':
					dislikes = review_data['data']['allReviews'][1]['count']
				else:
					pass
			except:
				dislikes = 0
			
		elif review_data['data']['allReviews'][0]['contentReviewValue'] == 'DISLIKE':
			dislikes = review_data['data']['allReviews'][0]['count']
			likes = 0
	except:
		likes = 0
		dislikes = 0

	rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes ='+str(likes)+'</h3><h3 style="background-color:powderblue;">Dislikes ='+str(dislikes)+'</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'
	answer = answer.replace('\n','<br>')							

	with open(completeName,'w', encoding='UTF-8') as e:
		e.write(html)
		e.write(rating)
		e.write('<head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>')
		e.write('<div class="container">'+str(question)+'</div>')
		e.write('<div class="container">'+answer+'</div>')
		e.write(webhook_script)
		e.close()
	
	
			
		
	
def process_ec(jfile,COOKIE,headers,question,webhook_script,completeName):
	
	print('[*] Answer type : E C Answer')
	#try:
	#	question = '<p><strong>Question</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['content']['body']+'</p><br></br>'
	#except:
	#	question = '<p><strong>Question</strong></p><p> There is an error in loading the question </p><br></br>'
	question = BeautifulSoup(question, 'html.parser')
	links = []
	for img in question.findAll('img'):
		if img.get('src').startswith("//"):
			print(img)
			img['src'] = img['src'].replace('//', 'https://')
			try:
				img['style'] =  img['style'].replace('height', 'h')
			except:
				pass
			print(img['src'])

	question = str(question)
	final_answer = '<p><strong>Final Answer</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['answerData']['finalAnswerHtml'][0]+'</p>'
	final_answer = BeautifulSoup(final_answer, 'html.parser')
	links = []
	for img in final_answer.findAll('img'):
		if img.get('src').startswith("//"):
			print(img)
			img['src'] = img['src'].replace('//', 'https://')
			try:
				img['style'] =  img['style'].replace('height', 'h')
			except:
				pass
			print(img['src'])

	final_answer = str(final_answer)
	legacy_id = jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['legacyId']
	general_guidance = '<p><strong>General Guidance</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['answerData']['generalGuidance'][0]['html']+'</p>'
	steps = jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['answerData']['steps']
	all_steps = []
	
	for x in range(len(steps)):
		print(x)
		step = '<div class="container">'+jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['answerData']['steps'][x]['textHtml']+'</div>'
		explanation = '<div class="container"><p><strong>Explanation</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['ecAnswers'][0]['answerData']['steps'][x]['explanationHtml']+'</p></div>'

		all_steps.append(step)
		all_steps.append(explanation)
	
	steps = ''.join(all_steps)
	

	review_data = {
		'operationName': 'ReviewsV2',
		'variables': {
			'reviewForContentQueryArguments': {
				'contentId': str(legacy_id),
				'contentReviewType': 'LIKE_DISLIKE',
				'contentType': 'ANSWER',
			},
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1',
			},
		},
	}
	response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=COOKIE, headers=headers, json=review_data)
	review_data = json.loads(response.content)

	try:
		if review_data['data']['allReviews'][0]['contentReviewValue'] == 'LIKE':
			likes = review_data['data']['allReviews'][0]['count']
			try:
				if review_data['data']['allReviews'][1]['contentReviewValue'] == 'DISLIKE':
					dislikes = review_data['data']['allReviews'][1]['count']
				else:
					pass
			except:
				dislikes = 0
			
		elif review_data['data']['allReviews'][0]['contentReviewValue'] == 'DISLIKE':
			dislikes = review_data['data']['allReviews'][0]['count']
			likes = 0
	except:
		likes = 0
		dislikes = 0

	rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes ='+str(likes)+'</h3><h3 style="background-color:powderblue;">Dislikes ='+str(dislikes)+'</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'
	

	
	
	with open (completeName,'w', encoding='utf-8') as f:
		f.write(rating)
		f.write('<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>')					
		f.write('<div class="question">'+str(question)+'</div>')
		f.write('<div class="container">'+str(general_guidance)+'</div>')
		f.write(str(steps))
		f.write('<div class="container">'+str(final_answer)+'</div>')
		f.write(webhook_script)
		f.close()
		
		
			
		
def process_html(jfile,COOKIE,headers,question,webhook_script,completeName):
	print('[*] Answer type : HTML Answer')
	
	#try:
	#	question = '<p><strong>Question</strong></p><p>'+jfile['data']['questionByLegacyId']['displayAnswers']['content']['body']+'</p><br></br>'
	#except:
	#	question = '<p><strong>Question</strong></p><p> There is an error in loading the question </p><br></br>'
	question = BeautifulSoup(question, 'html.parser')
	
	links = []
	
	try:
		for img in question.findAll('img'):
			if img.get('src').startswith("//"):
				print(img)
				img['src'] = img['src'].replace('//', 'https://')
				try:
					img['style'] =  img['style'].replace('height', 'h')
				except:
					pass
				print(img['src'])
		question = str(question)
	except:
		question = str(question)
	legacy_id = jfile['data']['questionByLegacyId']['displayAnswers']['htmlAnswers'][0]['legacyId']
	html = jfile['data']['questionByLegacyId']['displayAnswers']['htmlAnswers'][0]['answerData']['html']
	html = BeautifulSoup(html, 'html.parser')
	
	links = []
	for img in html.findAll('img'):
		if img.get('src').startswith("//"):
			print(img)
			img['src'] = img['src'].replace('//', 'https://')
			try:
				img['style'] =  img['style'].replace('height', 'h')
			except:
				pass
			print(img['src'])

	html = str(html)
	
	review_data = {
		'operationName': 'ReviewsV2',
		'variables': {
			'reviewForContentQueryArguments': {
				'contentId': str(legacy_id),
				'contentReviewType': 'LIKE_DISLIKE',
				'contentType': 'ANSWER',
			},
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1',
			},
		},
	}
	response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=COOKIE, headers=headers, json=review_data)
	review_data = json.loads(response.content)

	try:
		if review_data['data']['allReviews'][0]['contentReviewValue'] == 'LIKE':
			likes = review_data['data']['allReviews'][0]['count']
			try:
				if review_data['data']['allReviews'][1]['contentReviewValue'] == 'DISLIKE':
					dislikes = review_data['data']['allReviews'][1]['count']
				else:
					pass
			except:
				dislikes = 0
			
		elif review_data['data']['allReviews'][0]['contentReviewValue'] == 'DISLIKE':
			dislikes = review_data['data']['allReviews'][0]['count']
			likes = 0
	except:
		likes = 0
		dislikes = 0
	rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes ='+str(likes)+'</h3><h3 style="background-color:powderblue;">Dislikes ='+str(dislikes)+'</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'
	ansCount = jfile['data']['questionByLegacyId']['displayAnswers']['htmlAnswers'][0]['answerData']['author']['answerCount']
	
	
	with open(completeName, 'w', encoding='utf-8') as f:
		f.write(rating)
		f.write('<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>')
		f.write('<div class="question">'+str(question)+'</div>')
		f.write('<div class="container"><p><strong>Answer</strong></p><p>Total answers posted by the expert is: '+str(ansCount)+'</p>'+str(html)+'</div>')
		f.write(webhook_script)
		f.close()
		

		
def process_sqna(jfile,COOKIE,headers,question,webhook_script,completeName):
	
	print('[*] Answer type : SQNA Answer')
								
	
	data = json.loads(jfile['data']['questionByLegacyId']['displayAnswers']['sqnaAnswers']['answerData'][0]['body']['text'])
	with open('table.json','w') as f:
		f.write(json.dumps(data,indent=4))
		f.close()

	#bloc_eq = data['stepByStep']['steps'][0]['blocks'][0]['block']['editorContentState']['entityMap']


	number_of_steps = range(len(data['stepByStep']['steps']))
	number_of_final_answers = range(len(data['finalAnswer']['blocks']))


	ans = []
	explanation = []
	code_data_html = ['']
	for count in number_of_steps:
		ans.append('<div class="steps">Step '+str(count+1)+' of '+str(len(number_of_steps))+'</div>')
		block_content = data['stepByStep']['steps'][count]['blocks']
		number_of_blocks = range(len(block_content))
		
		try:
			number_of_explanation = range(len(data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks']))
		except Exception as e:

			number_of_explanation = range(0)
		print('>> Step: '+str(count+1))
		for x in number_of_blocks:
			block_type = data['stepByStep']['steps'][count]['blocks'][x]['type']
			
			print('[*] Block Type : '+block_type)

	#_________________________________ CHECK TEXT ________________________________________________________


			if block_type == 'TEXT':
				
				try:
				
					check_version = data['stepByStep']['steps'][count]['blocks'][x]['block']['version']
				except:
					check_version = ''
					
				if check_version == '1.2.0' or check_version == '':
				
					number_of_ptags = range(len(data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks']))
					for y in number_of_ptags:
						ptag = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['text']
						print(ptag)
						entityRanges = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges']
						preset = 0
						if len(entityRanges) != 0:
							number_of_entity_ranges = range(len(data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges']))
							
							eq_length = 0
							
							for n in number_of_entity_ranges:
								offset = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges'][n]['offset']
								key = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges'][n]['key']
								inline_equation_type = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['entityMap'][str(key)]['type']
								#MADE CHANGES HERE MAY 19
								if inline_equation_type == 'CHEM-INLINE-EQUATION':
									inline_equation = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['entityMap'][str(key)]['data']['text']
								else:
									inline_equation = ' `'+data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['entityMap'][str(key)]['data']['text']+'` '
								
								ptag = list(ptag)
								ptag.insert(offset, inline_equation)

							ptag = ''.join(ptag)
							#ans.append(ptag)
								
						else:
							#ans.append(ptag)
							pass
						
						inlineStyleRanges = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges']
						if len(inlineStyleRanges) != 0:
							
							for styles in range(len(inlineStyleRanges)):
								style = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['style']
								length = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['length']
								offset = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['offset']
								
								if style == 'BOLD':
									ptag = '<strong>'+str(ptag)+'</strong>'
								elif style == 'ITALIC':
									ptag = '<i>'+str(ptag)+'</i>'
								elif style == 'UNDERLINE':
									ptag = '<u>'+str(ptag)+'</u>'
									pass
						ans.append(ptag)
									
				
				
				elif check_version == '2.0.0':
					
					
					contents = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']
					
					target_key = "text"
					desired_values = find_text(contents, target_key)
					
					
					content_list = []
					
					for i in desired_values:
						content_list.append('<p>')
						for content in desired_values[i]:
							
							if '`' in content['text']:
								content['text'] = content['text'].replace('`',"'")
							
							if content['type'] == 'inlineMath':
								content_list.append('`'+content['text']+'`')
							elif content['type'] == 'paragraph':
								content_list.append(content['text'])
							else:
								pass
						content_list.append('</p>')
					
					ans.append(f'{"".join(content_list)}')
					
									
				else:
					ans.append('<h1>ERROR, INFORM @THE_ADMIN_FREEPORT</h1>')
							
							
						
			
			
			elif block_type == 'EXPLANATION':
				
				try:
					check_version = data['stepByStep']['steps'][count]['blocks'][x]['block']['version']
				except:
					check_version = ''
					
				if check_version == '1.2.0' or check_version == '':
				
				
				
					number_of_ptags = range(len(data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks']))
					ans.append('<div class="explanation" style="margin-left:30px;"><p><b>Explanation</b></p>')
					for y in number_of_ptags:
						
						ptag = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['text']
						if ptag != "":
							entityRanges = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges']
							preset = 0
							if len(entityRanges) != 0:
								number_of_entity_ranges = range(len(data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges']))
								
								eq_length = 0
								
								for n in number_of_entity_ranges:
									offset = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges'][n]['offset']
									key = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['entityRanges'][n]['key']
									inline_equation = ' `'+data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['entityMap'][str(key)]['data']['text']+'` '
									 
									ptag = list(ptag)
									ptag.insert(offset, inline_equation)

								ptag = ''.join(ptag)
								#ans.append(ptag)
									
							else:
								#ans.append(ptag)
								pass
							
							inlineStyleRanges = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges']
							if len(inlineStyleRanges) != 0:
								
								for styles in range(len(inlineStyleRanges)):
									style = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['style']
									length = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['length']
									offset = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']['blocks'][y]['inlineStyleRanges'][styles]['offset']
									
									if style == 'BOLD':
										ptag = '<strong>'+str(ptag)+'</strong>'
									elif style == 'ITALIC':
										ptag = '<i>'+str(ptag)+'</i>'
									elif style == 'UNDERLINE':
										ptag = '<u>'+str(ptag)+'</u>'
										pass
							ans.append('<p>'+ptag+'</p>')
					ans.append('</div>')
				
				elif check_version == '2.0.0':
					
					ans.append('<div class="explanation" style="margin-left:30px;"><p><b>Explanation</b></p>')
					contents = data['stepByStep']['steps'][count]['blocks'][x]['block']['editorContentState']
					
					target_key = "text"
					desired_values = find_text(contents, target_key)
					
					content_list = []
					
					for i in desired_values:
						content_list.append('<p>')
						for content in desired_values[i]:
							
							if '`' in content['text']:
								content['text'] = content['text'].replace('`',"'")
							
							if content['type'] == 'inlineMath':
								content_list.append('`'+content['text']+'`')
							elif content['type'] == 'paragraph':
								content_list.append(content['text'])
							else:
								pass
						content_list.append('</p>')
					
					ans.append(f'{"".join(content_list)}</div>')
					
						
				else:
					ans.append('<h1>ERROR, INFORM @THE_ADMIN_FREEPORT</h1>')
			
			
			elif block_type == 'MATH_IN_TEXT':
				
				
				try:
					check_version = data['stepByStep']['steps'][count]['blocks'][x]['block']['version']
				except:
					check_version = ''
				
				if check_version == '1.2.0' or check_version == '1.3.0':
					math_in_text = []
					title_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['title']['editorContentState']['blocks']
					
					for y in range(len(title_block)):
						title = '`\ text{'+str(title_block[y]['text'])+'}`'
						math_in_text.append(title)
						
					
					expression_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['expression']['editorContentState']['blocks']
					
					for z in range(len(expression_block)):
						math_in_text.append(' = ')
						expression = '`\ text{'+str(expression_block[z]['text'])+'}`<br>'
						math_in_text.append(expression)
					
					result_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['result']['editorContentState']['blocks']
					
					for result in range(len(result_block)):
						result = '`\ text{ = '+str(result_block[result]['text'])+'}`'
						math_in_text.append(result)
					
					dat ='<p>'+str(''.join(math_in_text))+'</p>'
					ans.append(dat)
				
				elif check_version == '2.0.0':
					math_in_text = []
					title_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['title']
					
					target_key = "text"
					desired_values = find_text(title_block, target_key)
					
					for i in desired_values:
						for content in desired_values[i]:
							title = '`\ text{'+str(content['text'])+'}`'
					math_in_text.append(title)
					
					math_in_text.append(' = ')
					expression_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['expression']
					
					target_key = "text"
					desired_values = find_text(expression_block, target_key)
					
					for i in desired_values:
						for content in desired_values[i]:
							expression = '`\ text{'+str(content['text'])+'}`<br>'
					math_in_text.append(expression)
					
					result_block = data['stepByStep']['steps'][count]['blocks'][x]['block']['result']
					
					target_key = "text"
					desired_values = find_text(result_block, target_key)
					
					for i in desired_values:
						for content in desired_values[i]:
							result = '`\ text{ = '+str(content['text'])+'}`'
					math_in_text.append(result)
					
					dat ='<p>'+str(''.join(math_in_text))+'</p>'
					ans.append(dat)
				
				
	#_________________________________ CHECK IMAGE _______________________________________________________


		
			elif block_type == 'IMAGE_UPLOAD':
				image_path = data['stepByStep']['steps'][count]['blocks'][x]['block']['imagePath']
				ans.append('<img src="'+str(image_path)+'">')
				
				

				
	#_________________________________ CHECK DRAWING _____________________________________________________

	
			elif block_type == 'DRAWING':
				
				viewbox_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['settings']['viewBox']
				v_x = viewbox_data['x']
				v_y = viewbox_data['y']
				v_w = viewbox_data['w']
				v_h = viewbox_data['h']
				
				v_html = '''<svg data-test="svg" viewBox="{} {} {} {}" width="{}" class="sc-1wwe652-1 dZTFxH"'''.format(v_x,v_y,v_w,v_h,v_w)
				ans.append(v_html)




	#_________________________________ CHECK TABLE _______________________________________________________


		
			elif block_type == 'TABLE':
				matrix=[]
				row=[]
				
				c = data['stepByStep']['steps'][count]['blocks'][x]['block']['columns']
				r = data['stepByStep']['steps'][count]['blocks'][x]['block']['rows']
				
				
				for i in range(r):
					row=[]
					for j in range(c):
						row.append('')
					matrix.append(row)
				
				
				column_properties = []
				column_span_list = data['stepByStep']['steps'][count]['blocks'][x]['block']['columnSpans']
				
				for c in range(len(column_span_list)):
					cSpan_data = list(column_span_list)[c]
					
					row = int(list(column_span_list)[c].split('-')[1])
					column = int(list(column_span_list)[c].split('-')[0])
					c_data = str(column)+'-'+str(row)
					column_properties.append(c_data)
					
						
				table_cells = data['stepByStep']['steps'][count]['blocks'][x]['block']['cells']
				try:
					table_cells_version = data['stepByStep']['steps'][count]['blocks'][x]['block']['version']
				except:
					table_cells_version = ''
					
				if table_cells_version == '2.0.0':
					print('[*] Table version 2.0.0')
					
					
					
					for j in range(len(table_cells)):
						
						
						t_data = list(table_cells)[j]
						
						
						cells_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['cells'][t_data]
						
						
						target_key = "text"
						main_cell_data = find_text(cells_data, target_key)
						
						cell_data_list = []
						
						for i in main_cell_data:
							
							for content in main_cell_data[i]:
								if content['type'] == 'inlineMath':
									cell_data_list.append(' `'+content['text']+'` ')
								elif content['type'] == 'paragraph':
									cell_data_list.append(content['text'])

								else:
									pass
							
						cell_data = ''.join(cell_data_list)
						
						
						if len(main_cell_data) ==0:

							cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+' '
						
						else:
							
							if t_data in column_properties:
								
								cell_data = str(data['stepByStep']['steps'][count]['blocks'][x]['block']['columnSpans'][t_data])+' style="border: 1px solid #666666;text-align:center;">'+cell_data
								
							else:
								
								cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+cell_data
						
					
						try:
							row = int(list(table_cells)[j].split('-')[1])
							column = int(list(table_cells)[j].split('-')[0])

							matrix = np.array(matrix,dtype=object)
							matrix_T = matrix.T
							list(matrix_T)[column][row] = cell_data
							
							
							matrix = matrix_T.T
							
							
						except:
							pass
						
				
					
				
				
				else:
					print('[*] Table version 1.2.0')
					for j in range(len(table_cells)):
						
						
						t_data = list(table_cells)[j]
						cell_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['cells'][t_data]['value']['blocks'][0]['text']
						
						
						
						
						try:
							styles = data['stepByStep']['steps'][count]['blocks'][x]['block']['cells'][t_data]['value']['blocks'][0]['inlineStyleRanges']
							
							for style in range(len(styles)):
								if styles[style]['style']=='BOLD':
									cell_data = '<strong>'+str(cell_data)+'</strong>'
								elif styles[style]['style']=='ITALIC':
									cell_data = '<em>'+str(cell_data)+'</em>'
						except Exception as e:
							print(e)
							pass
						if t_data in column_properties:
							
							cell_data = str(data['stepByStep']['steps'][count]['blocks'][x]['block']['columnSpans'][t_data])+' style="border: 1px solid #666666;text-align:center;">'+cell_data
							
							
						else:
							
							if len(cell_data) ==0:

								cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+' '

								
							else:
								cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+cell_data
								pass
							pass
						try:
							row = int(list(table_cells)[j].split('-')[1])
							column = int(list(table_cells)[j].split('-')[0])

							matrix = np.array(matrix,dtype=object)
							matrix_T = matrix.T
							list(matrix_T)[column][row] = cell_data
							matrix = matrix_T.T
						except:
							pass
					
					
					
				ar = matrix.T
				html = """<html><body><table id='tb1' style="width:100%; border-collapse: collapse;"><tbody id='tb'>{}</tbody></table></body></html>"""

				r = ''

				for x in range(len(matrix)):
			
					
					r+=('<tr>{}</tr>'.format(
										''.join(["<td colspan="+l[x]+"</td>" for l in ar])))

				html = html.format(r)
				ans.append(html)

				


    #_________________________________ CHECK ACCOUNTING TABLE ____________________________________________
    
    
    
			elif block_type == 'ACCOUNTING_TABLE':
				
				matrix = []
				row = []
				
				header_cells = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells']
				
				if header_cells != {}:
					column_list = []
					for cell in header_cells:
						
						column = cell.split('-')[0]
						column_list.append(int(column))
						
					sort_column_list = column_list.sort()
					
					c = column_list[-1]+1
					
					
				body_cells = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells']
				row_list = []
				for cell in body_cells:
					
					row = cell.split('-')[1]
					row_list.append(int(row))
					
				sort_row_list = row_list.sort()
				r = row_list[-1]+1
				
				for i in range(r):
					row=[]
					for j in range(c):
						row.append('')
					matrix.append(row)
				
				for cell in header_cells:
					cell_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['value']
					css_style = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css']
					
					#Finding the css elements of the cells
					for css in css_style:
						
						if css == 'border':
							border = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'textAlign':
							text_align = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'fontweight':
							font_weight = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'fontSize':
							font_size = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'width':
							width = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'height':
							height = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						elif css == 'borderBottom':
							border_bottom = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['headerCells'][cell]['style']['css'][css]
						else:
							
							text_align = ''
							font_weight = ''
							font_size = ''
							width = ''
							height = ''
							border_bottom = ''
							
					###############################################
					
					
					column = int(cell.split('-')[0])
					row = int(cell.split('-')[1])
					matrix = np.array(matrix,dtype=object)
					matrix_T = matrix.T
					list(matrix_T)[column][row] = f'0 style="border: {border};text-align:{text_align};width:{width};height:{height};font-weight:{font_weight};font-size:{font_size};border-bottom:{border_bottom};">'+str(cell_data)
					matrix = matrix_T.T
				
				header_cell_matrix = matrix[0]
				
					
				
				for cell in body_cells:
					
					cell_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['value']
					cell_type = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['type']
					css_style = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css']
					
					#Finding the css elements of the cells
					
					style_dict = {
									"border":None,
									"text_align":None,
									"font_weight":None,
									"font_size":None,
									"width":None,
									"height":None,
									"border_bottom":None,
									"vertical_align":None,
									"border_right":''
								}
								
					for css in css_style:
						
						if css == 'border':
							border = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["border"] = border
						elif css == 'textAlign':
							text_align = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["text_align"] = text_align
						elif css == 'fontweight':
							font_weight = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["font_weight"] = font_weight
						elif css == 'fontSize':
							font_size = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["font_size"] = font_size
						elif css == 'width':
							width = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["width"] = width
						elif css == 'height':
							height = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["height"] = height
						elif css == 'borderBottom':
							border_bottom = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["border_bottom"] = border_bottom
						elif css == 'verticalAlign':
							vertical_align = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["vertical_align"] = vertical_align
						elif css == 'borderRight':
							border_right = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['css'][css]
							style_dict["border_right"] = border_right
						else:
							
							pass
					
					###############################################
	
					
					#Finding if there is any col span or row span	
					try:
						css_span = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['style']['span']
						try:
							col_span = css_span['colSpan']
						except:
							col_span = '0'
							pass
						try:
							row_span = css_span['rowSpan']
						except:
							pass
					except:
						col_span = '0'
						row_span = '0'
						pass
					##############################################
					
					
					#Checking if the cell is empty or the cell has extra elements like editorcontentstate
					if cell_type == 'NONE':
						cell_data = ' '
					
					if cell_data == None:
						cell_data = ' '
						
					elif type(cell_data) is dict:
						try:
							cell_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['value']['editorContentState']['blocks'][0]['text']
							text_type = data['stepByStep']['steps'][count]['blocks'][x]['block']['entries'][0]['bodyCells'][cell]['value']['editorContentState']['blocks'][0]['type']
						except:
							
							
							desired_values = find_text(cell_data, 'text')
							
							if desired_values != {}:
								for i in desired_values:
									
									for content in desired_values[i]:
										cell_data = content['text']
							else:
								cell_data = ''
							
					else:
						pass
					
					##############################################
					
					
					column = int(cell.split('-')[0])
					row = int(cell.split('-')[1])
					matrix = np.array(matrix,dtype=object)
					matrix_T = matrix.T
					list(matrix_T)[column][row] = f'{col_span} style="vertical-align:{style_dict["vertical_align"]}; border: {style_dict["border"]};text-align:{style_dict["text_align"]};width:{style_dict["width"]};height:{style_dict["height"]};font-weight:{style_dict["font_weight"]};font-size:{style_dict["font_size"]};border-bottom:{style_dict["border_bottom"]};border-right:{style_dict["border_right"]};">'+str(cell_data)
					matrix = matrix_T.T
				
				matrix = np.array(matrix)
				matrix = np.insert(matrix, 0, np.array(header_cell_matrix), axis=0)
					
					
				ar = matrix.T
				html = """<html><body><table id='tb1' style="width:100%; border-collapse: collapse;"><tbody id='tb'>{}</tbody></table></body></html>"""

				r = ''

				for x in range(len(matrix)):
			
					
					r+=('<tr>{}</tr>'.format(
										''.join(["<td colspan="+l[x]+"</td>" for l in ar])))

				html = html.format(r)
				ans.append(html)
				
				
	#_________________________________ CHECK EQUATION RENDERER ___________________________________________

				
				
			elif block_type == 'EQUATION_RENDERER':
				
				
				number_of_main_eq = range(len(data['stepByStep']['steps'][count]['blocks'][x]['block']['lines']))
				
				for eq in number_of_main_eq:
					LHS = data['stepByStep']['steps'][count]['blocks'][x]['block']['lines'][eq]['left']
					RHS = data['stepByStep']['steps'][count]['blocks'][x]['block']['lines'][eq]['right']
					operator = data['stepByStep']['steps'][count]['blocks'][x]['block']['lines'][eq]['operator']
					
					equation = '`'+LHS+' '+operator+' '+RHS+'`'
					ans.append(equation)


	#_________________________________ CHECK CODE SNIPPET ________________________________________________


		
			elif block_type == 'CODE_SNIPPET':
				try:
					
					check_version = data['stepByStep']['steps'][count]['blocks'][x]['block']['version']
				except:
					check_version = ''
				
				if check_version == '2.0.0':
					
					contents = data['stepByStep']['steps'][count]['blocks'][x]['block']
					
					target_key = "text"
					desired_values = find_text(contents, target_key)
					print(desired_values)
					
					cd_data = []
					ans.append('CODE_SNIPPET_PLACEHOLDER')
					
					temp = []
					for i in desired_values:
						
						temp.append(desired_values[i][0]['text'])
					
					code_data = ''.join(temp).split('\n')
					for c_data in code_data:
						codeData = '<code>'+str(c_data)+'</code>\n'
						cd_data.append(codeData)
					code_data_html.append(''.join(cd_data))
					
				
				else:
				
					cd_data = []
					ans.append('CODE_SNIPPET_PLACEHOLDER')
					code_data = data['stepByStep']['steps'][count]['blocks'][x]['block']['codeData'].split('\n')
					for c_data in code_data:
						codeData = '<code>'+str(c_data)+'</code>\n'
						cd_data.append(codeData)
					code_data_html.append(''.join(cd_data))

				
		
		
		for num in number_of_explanation:
			exp = data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks'][num]['text']
			
			exp_entityRanges = data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks'][num]['entityRanges']
			number_of_explanation_eq = range(len(data['stepByStep']['steps'][count]['explanation']['editorContentState']['entityMap']))
			
			if len(exp_entityRanges) != 0:
				number_of_entity_ranges = range(len(data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks'][num]['entityRanges']))
				preset = 0

				for n in number_of_entity_ranges:
					offset = data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks'][num]['entityRanges'][n]['offset']
					key = data['stepByStep']['steps'][count]['explanation']['editorContentState']['blocks'][num]['entityRanges'][n]['key']
					inline_equation = ' `'+data['stepByStep']['steps'][count]['explanation']['editorContentState']['entityMap'][str(key)]['data']['text']+'` '

					exp = list(exp)
					exp.insert(offset, inline_equation)

				exp = ''.join(exp)
				ans.append(exp)
			else:
				ans.append(exp)
				pass
				



	ans.append('<h3>Final Answer</h3>')
	for count in number_of_final_answers:
		
		final_block_type = data['finalAnswer']['blocks'][count]['type']
		
		try:
			check_version = data['finalAnswer']['blocks'][count]['block']['version']
		except:
			check_version = ''
					
		if check_version == '1.2.0' or check_version == '':
		
			print('hey')
			if final_block_type == "TEXT":
				
				content = data['finalAnswer']['blocks'][count]
				final_ans_count = range(len(data['finalAnswer']['blocks'][count]['block']['editorContentState']['blocks']))
				
				for counts in final_ans_count:
					fin_ans = str(data['finalAnswer']['blocks'][count]['block']['editorContentState']['blocks'][counts]['text'])
					
					
					fin_exp_entityRanges = data['finalAnswer']['blocks'][count]['block']['editorContentState']['blocks'][counts]['entityRanges']
					if len(fin_exp_entityRanges) != 0:
						for m in range(len(fin_exp_entityRanges)):
							print(m)
							offset = data['finalAnswer']['blocks'][count]['block']['editorContentState']['blocks'][counts]['entityRanges'][m]['offset']
							key = data['finalAnswer']['blocks'][count]['block']['editorContentState']['blocks'][counts]['entityRanges'][m]['key']
							inline_equation = ' `'+data['finalAnswer']['blocks'][count]['block']['editorContentState']['entityMap'][str(key)]['data']['text']+'` '

							fin_ans = list(fin_ans)
							fin_ans.insert(offset, inline_equation)

						fin_ans = ''.join(fin_ans)
						ans.append(fin_ans)
					else:
						ans.append(fin_ans)
		
		elif check_version == '2.0.0':
			
			if final_block_type == "TEXT":
			
				ans.append('<p>')
				
				main_block = data['finalAnswer']['blocks'][count]['block']
				
				target_key = "text"
				desired_values = find_text(main_block, target_key)
				
				
				for i in desired_values:
					ans.append('<p>')
					for content in desired_values[i]:
						if content['type'] == 'inlineMath':
							ans.append(' `'+content['text']+'` ')
						elif content['type'] == 'paragraph':
							ans.append(content['text'])

						else:
							pass
					ans.append('</p>')
			
			elif final_block_type == "CODE_SNIPPET":
				
				try:
					
					check_version = data['finalAnswer']['blocks'][count]['block']['version']
				except:
					check_version = ''
				
				if check_version == '2.0.0':
					
					contents = data['finalAnswer']['blocks'][count]['block']
					
					target_key = "text"
					desired_values = find_text(contents, target_key)
					print(desired_values)
					
					cd_data = []
					ans.append('CODE_SNIPPET_PLACEHOLDER')
					
					temp = []
					for i in desired_values:
						
						temp.append(desired_values[i][0]['text'])
					
					code_data = ''.join(temp).split('\n')
					for c_data in code_data:
						codeData = '<code>'+str(c_data)+'</code>\n'
						cd_data.append(codeData)
					code_data_html.append(''.join(cd_data))
					
				
				else:
				
					cd_data = []
					ans.append('CODE_SNIPPET_PLACEHOLDER')
					code_data = data['finalAnswer']['blocks'][count]['blocks'][x]['block']['codeData'].split('\n')
					for c_data in code_data:
						codeData = '<code>'+str(c_data)+'</code>\n'
						cd_data.append(codeData)
					code_data_html.append(''.join(cd_data))
				
		
		elif check_version == '1.6.0':
			
			if final_block_type == "TABLE":
				
				matrix=[]
				row=[]
				
				c = data['finalAnswer']['blocks'][count]['block']['columns']
				r = data['finalAnswer']['blocks'][count]['block']['rows']
				for i in range(r):
					row=[]
					for j in range(c):
						row.append('')
					matrix.append(row)
				
				column_properties = []
				column_span_list = data['finalAnswer']['blocks'][count]['block']['columnSpans']
				
				for c in range(len(column_span_list)):
					cSpan_data = list(column_span_list)[c]
					
					row = int(list(column_span_list)[c].split('-')[1])
					column = int(list(column_span_list)[c].split('-')[0])
					c_data = str(column)+'-'+str(row)
					column_properties.append(c_data)
					
						
				table_cells = data['finalAnswer']['blocks'][count]['block']['cells']
				try:
					table_cells_version = data['finalAnswer']['blocks'][count]['block']['version']
				except:
					table_cells_version = ''
				
				if table_cells_version == '1.6.0':
				
					for j in range(len(table_cells)):
							
							
						t_data = list(table_cells)[j]
						cell_data = data['finalAnswer']['blocks'][count]['block']['cells'][t_data]['value']['blocks'][0]['text']
						
						
						
						
						try:
							styles = data['finalAnswer']['blocks'][count]['block']['cells'][t_data]['value']['blocks'][0]['inlineStyleRanges']
							
							for style in range(len(styles)):
								if styles[style]['style']=='BOLD':
									cell_data = '<strong>'+str(cell_data)+'</strong>'
								elif styles[style]['style']=='ITALIC':
									cell_data = '<em>'+str(cell_data)+'</em>'
						except Exception as e:
							print(e)
							pass
						if t_data in column_properties:
							
							cell_data = str(data['finalAnswer']['blocks'][count]['block']['columnSpans'][t_data])+' style="border: 1px solid #666666;text-align:center;">'+cell_data
							
							
						else:
							
							if len(cell_data) ==0:

								cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+' '

								
							else:
								cell_data = '0 style="border: 1px solid #666666;text-align:center;">'+cell_data
								pass
							pass
						try:
							row = int(list(table_cells)[j].split('-')[1])
							column = int(list(table_cells)[j].split('-')[0])

							matrix = np.array(matrix,dtype=object)
							matrix_T = matrix.T
							list(matrix_T)[column][row] = cell_data
							matrix = matrix_T.T
						except:
							pass
					
					
				
			ar = matrix.T
			html = """<html><body><table id='tb1' style="width:100%; border-collapse: collapse;"><tbody id='tb'>{}</tbody></table></body></html>"""

			r = ''

			for x in range(len(matrix)):
		
				
				r+=('<tr>{}</tr>'.format(
									''.join(["<td colspan="+l[x]+"</td>" for l in ar])))

			html = html.format(r)
			ans.append(html)
			
			pass

			
			
	stepByStep = ['<h3>Steps</h3>']
	for x in ans:
		stepByStep.append('<p>'+x+'</p>')
	loop = 1
	for i in range(len(stepByStep)):
		if stepByStep[i] == '<p>CODE_SNIPPET_PLACEHOLDER</p>':
			
			stepByStep[i] = '<pre class="code">'+code_data_html[loop]+'</pre>'
			loop+=1
			print(loop)
		else:
			pass
			


	answer = unicodedata.normalize("NFKD", str(''.join(stepByStep)))

	html = '''<html>
	<head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width">
	  <title>MathJax example</title>
	 <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>
	<style>pre.code {
	  white-space: pre-wrap;
		background-color:#ededed;
	display: inline-block;
	width: 65em;
		padding-left: auto; /* now works */
	  margin-left: 10;  /* now works */

	}
	pre.code::before {
	  counter-reset: listing;

	}
	pre.code code {
	  counter-increment: listing;
	}
	pre.code code::before {
	  content: counter(listing) " ";
	  display: inline-block;
	  width: 2em;         /* now works */
	  padding-left: auto; /* now works */
	  margin-left: auto;  /* now works */
	  text-align: right;  /* now works */
		background-color:#d9d7d7;
	color:red;
	}
	</style>
	<style>p {
	  font-family: "Leelawadee UI";
	}</style>
	<style>
	.steps {
		width: 100%;
		background-color: rgb(239, 245, 254);
		line-height: 1;
		font-size: 0.875rem;
		font-weight: bold;
		padding: 0.75rem 1rem;
		border: 1px solid rgb(231, 231, 231);
		box-sizing: border-box;
		display: flex;
		-webkit-box-pack: justify;
		justify-content: space-between;
		cursor: pointer;
	}
	</style>
	</head>
	<body>'''

	legacy_id = jfile['data']['questionByLegacyId']['displayAnswers']['sqnaAnswers']['answerData'][0]['legacyId']
	
	review_data  = {
		'operationName': 'ReviewsV2',
		'variables': {
			'reviewForContentQueryArguments': {
				'contentId': str(legacy_id),
				'contentReviewType': 'LIKE_DISLIKE',
				'contentType': 'ANSWER',
			},
		},
		'extensions': {
			'persistedQuery': {
				'version': 1,
				'sha256Hash': '9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1',
			},
		},
	}
	response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=COOKIE, headers=headers, json=review_data)
	review_data = json.loads(response.content)

	try:
		if review_data['data']['allReviews'][0]['contentReviewValue'] == 'LIKE':
			likes = review_data['data']['allReviews'][0]['count']
			try:
				if review_data['data']['allReviews'][1]['contentReviewValue'] == 'DISLIKE':
					dislikes = review_data['data']['allReviews'][1]['count']
				else:
					pass
			except:
				dislikes = 0
			
		elif review_data['data']['allReviews'][0]['contentReviewValue'] == 'DISLIKE':
			dislikes = review_data['data']['allReviews'][0]['count']
			likes = 0
	except:
		likes = 0
		dislikes = 0

	rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes ='+str(likes)+'</h3><h3 style="background-color:powderblue;">Dislikes ='+str(dislikes)+'</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'
	answer = answer.replace('\n','<br>')							

	with open(completeName,'w', encoding='UTF-8') as e:
		e.write(html)
		e.write(rating)
		e.write('<head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>')
		e.write('<div class="container">'+str(question)+'</div>')
		e.write('<div class="container">'+answer+'</div>')
		e.write(webhook_script)
		e.close()
