# -*- coding: utf-8 -*-
#  Created by ibireme on 13/3/30.
#  Copyright (c) 2015 ibireme.
#  This source code is licensed under the MIT-style license found in the
#  LICENSE file in the root directory of this source tree.

class oc_files_manager(object):
	"""docstring for oc_files_manager"""
	__slots__ = ('h_file_content', 'm_file_content')

	def __init__(self, **kw):
		super(oc_files_manager, self).__init__()
		for key, value in kw.iteritems():
			if key == 'h_file_content':
				self.h_file_content = value
			elif key == 'm_file_content':
				self.m_file_content = value
			else:
				pass	

# Json 
try: 
	import json
except ImportError: 
	import simplejson as json

def is_json(json_str):
	try:
		json.loads(json_str)
	except Exception, e:
		return False
	return True

def get_jsoninfo_dic(json_str):	
	try:
		return json.loads(json_str)	
	except Exception, e:
		return {}

# GUI 
import os, sys
from Tkinter import *
import Tkinter, tkMessageBox
from tkFileDialog import asksaveasfilename, askdirectory
from collections import OrderedDict

def wliu_Tk_Center(target_Tk):
	target_Tk.update()
	curWidth = target_Tk.winfo_reqwidth()
	curHeight = target_Tk.winfo_height()
	scnWidth,scnHeight = target_Tk.maxsize() 
	tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
	target_Tk.geometry(tmpcnf)

base_model_str = 'BaseModel'
class JsonNode_InputBox(Frame):
	"""docstring for JsonNode_InputBox"""
	def __init__(self, json_od, master=None):
		Frame.__init__(self, master)
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.pack()
		self.propertiesDict = {base_model_str : base_model_str}
		self.json_od = json_od
		self.config_exchange_info()
		self.createWidgets()

	def createWidgets(self):
		self.od_tuple = self.ex_od.popitem(last=True)
		self.label = Label(self, text=self.od_tuple[1])
		self.label.pack()
		self.textfield = Entry(self, width=36)
		self.textfield.bind("<Return>", self.click_entercommend)
		self.textfield.pack()
		self.enter_btn = Button(self, text = 'Enter', command=self.click_enterhandler)
		self.enter_btn.pack()			

	def click_entercommend(self, event):
		self.click_enterhandler()

	def click_enterhandler(self):
		save_key = self.od_tuple[0]
		text = self.textfield.get()
		self.propertiesDict[save_key] = text
		print '···%s<-config->%s complete' % (save_key, text)
		if len(self.ex_od) > 0:
			if len(self.ex_od) == 1:
				self.enter_btn['text'] = 'Out Put Files'
			self.od_tuple = self.ex_od.popitem(last=True)
			self.label['text'] = self.od_tuple[1]
			self.textfield.delete(0, END)
		else:
			self.outputFiles(self.json_od)
			self.showSuccess('转换成功！')
			self.quit()

	def config_exchange_info(self):
		self.ex_od = self.get_exchange_od(self.json_od)
		self.ex_od[base_model_str] = 'base model name'

	def get_exchange_od(self, json_OrderedDict):
		result_list = [] 
		for key, value in json_OrderedDict.iteritems():
			if isinstance(value, dict):
				title_tmp = '%s字段对应Class Name' % key
				result_list.append((key, title_tmp))
			elif isinstance(value, list):
				title_tmp = '%s字段对应数组的Member的Class Name' % key
				result_list.append((key, title_tmp))
		return OrderedDict(result_list)

	def get_propertyvalue(self, key):
		name = key
		try:
			name = self.propertiesDict[key]
			return name
		except Exception, e:
			return name

	def get_oderedlist_ocfiles_manager(self, json_OrderedDict, model_name):
		h_result_list = ['\n@interface %s : NSObject\n' % model_name]
		m_result_list = ['\n@implementation %s \n' % model_name]
		m_result_list.append('\n- (instancetype)initWith%sDic:(NSDictionary *)infoDic {\n\tself = [super init];\n\tif (self) {\n\t\tif (infoDic) {\n' % model_name)
		for key, value in json_OrderedDict.iteritems():
			if isinstance(value, dict):
				name = self.get_propertyvalue(key)
				
				h_result_list.append('\n@property (nonnull, nonatomic, strong) %s *%s;// %s\n' % (name ,key, value))
				m_result_list.append('\t\t\t_%s = [infoDic objectForKey:@"%s"];\n' % (key, key))

				model_list_manager = self.get_oderedlist_ocfiles_manager(value, name)
				h_result_list.insert(0, model_list_manager.h_file_content)
				m_result_list.insert(0, model_list_manager.m_file_content)
			elif isinstance(value, list):
				if len(value) > 0:
					target_obj = value[0]
					if isinstance(target_obj, dict):
						name = self.get_propertyvalue(key)

						h_result_list.append('\n@property (nonnull, nonatomic, strong) NSArray<%s *> *%s;// %s\n' % (name ,key, value))
						forin_str = 'NSMutableArray *resultArr = [@[] mutableCopy];\n\t\t\tNSArray *targetArr = [infoDic objectForKey:@"%s"];\n\t\t\tfor (NSDictionary *dic in targetArr) {\n\t\t\t\t%s *obj = [[%s alloc] initWith%sDic:dic];\n\t\t\t\t[resultArr addObject:obj];\n\t\t\t}' % (key, name, name, name)
						m_result_list.append('\n\t\t\t%s\n\t\t\t_%s = %s;\n' % (forin_str, key, '[resultArr copy]'))

						model_list_manager = self.get_oderedlist_ocfiles_manager(target_obj, name)
						h_result_list.insert(0, model_list_manager.h_file_content)
						m_result_list.insert(0, model_list_manager.m_file_content)
					elif isinstance(target_obj, basestring):
						print 'str arr'
					elif isinstance(target_obj, (int, long)):
						print 'integer arr'
					elif isinstance(target_obj, float):
						print 'float arr'

			elif isinstance(value, basestring):
				h_result_list.append('\n@property (nonnull, nonatomic, copy) NSString *%s;// %s\n' % (key, value))
				m_result_list.append('\t\t\t_%s = [infoDic objectForKey:@"%s"];\n' % (key, key))
			elif isinstance(value, (int, long)):
				h_result_list.append('\n@property (nonatomic, assign) NSInteger %s;// %d\n' % (key, value))
				m_result_list.append('\t\t\t_%s = [[infoDic objectForKey:@"%s"] integerValue];\n' % (key, key))
			elif isinstance(value, float):
				h_result_list.append('\n@property (nonatomic, assign) float %s; // %f\n' % (key, value))
				m_result_list.append('\t\t\t_%s = [[infoDic objectForKey:@"%s"] floatValue];\n' % (key, key))

		h_result_list.append('\n- (_Nonnull instancetype)initWith%sDic:(NSDictionary * _Nonnull)infoDic;\n\n@end\n' % model_name)
		m_result_list.append(('\n\t\t}\n\t}\n\treturn self;\n} \n\n@end\n\n\n'))
		oc_f = oc_files_manager(h_file_content=h_result_list, m_file_content=m_result_list)
		return oc_f

	def get_oderedstr(self, json_orderedlist):
		result_str = ''
		for x in json_orderedlist:
			if isinstance(x, basestring):
				result_str += x 
			elif isinstance(x, list):
				strTmp = result_str
				result_str = strTmp + self.get_oderedstr(x)
			else:
				pass
		return result_str

	def outputFiles(self, json_od):
		oc_list_manager = self.get_oderedlist_ocfiles_manager(self.json_od, self.propertiesDict[base_model_str])
		self.outputFile(self.get_oderedstr(oc_list_manager.h_file_content), '.h')
		self.outputFile(self.get_oderedstr(oc_list_manager.m_file_content),'.m')
		
	def outputFile(self, text, extension):
		options = {}
		options['initialfile'] = self.propertiesDict[base_model_str]+extension
		options['defaultextension'] = extension
		options['title'] = '%s file\'s name' % extension

		filename = asksaveasfilename(**options)
		if filename:
			if len(text) > 0:
				f1 = open(filename, 'w')
				if extension == '.h':
					prefix_str = '/*!\n *\tproducted by oc_json_plugin.py\n *\tauth: w6\n*/\n%s\n' % '#import <Foundation/Foundation.h>' 
				elif extension == '.m':
					header_str = ''
					try:
						header_str = os.path.split(filename)[-1].split('.')[0]+'.h'
						self.savename = os.path.split(filename)[-1].split('.')[0]
					except Exception, e:
						pass
					prefix_str = '/*!\n *\tproducted by oc_json_plugin.py\n *\tauth: w6\n */\n#import "%s"\n' % header_str 
				f1.write(prefix_str+text)
				f1.close()
			if extension == '.m':
				self.savepath = os.path.split(filename)[0]
				
	def showSuccess(self, msg):
		tkMessageBox.showinfo('Alert!', msg+'文件名为'+self.savename)
		os.system('open %s' % self.savepath)

class Appliction(Frame):
	"""docstring for Appliction"""
	def __init__(self, master=None):
		Frame.__init__(self, master)
		reload(sys)
		sys.setdefaultencoding('utf-8')
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.inputTextView = Text(self, width=166, height=36)
		self.inputTextView.bind("<Command-Key-a>", self.selectText)
		self.inputTextView.bind("<Command-Key-v>", self.onPaste)
		self.inputTextView.bind("<Command-Key-x>", self.onCut)
		self.inputTextView.bind("<Command-Key-c>", self.onCopy)
		self.inputTextView.pack(expand=0)
		self.checkBtn = Button(self, text = 'Exchange Json Node', command=self.pack_jsonnode_window)
		self.checkBtn.pack()

	def get_ordereddic(self, json_dic):
		obj_list = []
		objs_list = []
		properties_list = []
		for key, value in json_dic.iteritems():
			if isinstance(value, dict):
				obj_list.append((key, self.get_ordereddic(value)))
			elif isinstance(value, list):
				objs_list.append((key, value))
			elif isinstance(value, basestring):
				properties_list.append((key, value))
			elif isinstance(value, (int, long)):
				properties_list.append((key, value))
			elif isinstance(value, float):
				properties_list.append((key, value))

		od = OrderedDict(obj_list + objs_list + properties_list)
		return od

	def pack_jsonnode_window(self):
		alltext = self.inputTextView.get(1.0, END+'-1c')
		if is_json(alltext) == False: 
			self.showAlert('输入的是非法json')
			return
		info_dic = get_jsoninfo_dic(alltext)
		tmp_top = Toplevel()
		tmp_top.title('Exchange Window')
		tmp_top.wm_attributes("-topmost", 1)
		jn_ib = JsonNode_InputBox(self.get_ordereddic(info_dic), tmp_top)
		wliu_Tk_Center(tmp_top)
		jn_ib.pack()

	def selectText(self, event):
		self.inputTextView.tag_add(Tkinter.SEL, '1.0', Tkinter.END)
		return 'break';

	def onPaste(self, event):
		try:
			self.selection_get(selection='CLIPBOARD')
		except TclError:
			pass

	def onCut(self, event):
		self.onCopy(event)
		try:
			self.inputTextView.delete(SEL_FIRST, SEL_LAST)
		except Exception, e:
			pass
	
	def onCopy(self, event):
		try:
			text = self.inputTextView.get(SEL_FIRST, SEL_LAST)
			self.clipboard_clear()
			self.clipboard_append(text)
		except Exception, e:
			pass
		
	def showAlert(self, msg):
		tkMessageBox.showinfo('Waring!', msg)

root = Tk(className='Objective Json Plugin')
app = Appliction(root)
wliu_Tk_Center(root)
app.mainloop()  

try:
	root.destroy()
except Exception, e:
	pass

