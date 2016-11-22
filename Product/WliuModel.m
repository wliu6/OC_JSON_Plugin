/*!
 *	producted by oc_json_plugin.py
 *	auth: w6
 */
#import "WliuModel.h"

@implementation WliuTeam 

- (instancetype)initWithWliuTeamDic:(NSDictionary *)infoDic {
	self = [super init];
	if (self) {
		if (infoDic) {
			_count = [[infoDic objectForKey:@"count"] integerValue];
			_name = [infoDic objectForKey:@"name"];

		}
	}
	return self;
} 

@end



@implementation WliuResult 

- (instancetype)initWithWliuResultDic:(NSDictionary *)infoDic {
	self = [super init];
	if (self) {
		if (infoDic) {
			_url = [infoDic objectForKey:@"url"];
			_content = [infoDic objectForKey:@"content"];
			_version = [infoDic objectForKey:@"version"];
			_filesize = [[infoDic objectForKey:@"filesize"] floatValue];
			_isforce = [[infoDic objectForKey:@"isforce"] integerValue];

		}
	}
	return self;
} 

@end



@implementation WliuBaseModel 

- (instancetype)initWithWliuBaseModelDic:(NSDictionary *)infoDic {
	self = [super init];
	if (self) {
		if (infoDic) {
			_result = [infoDic objectForKey:@"result"];

			NSMutableArray *resultArr = [@[] mutableCopy];
			NSArray *targetArr = [infoDic objectForKey:@"team"];
			for (NSDictionary *dic in targetArr) {
				WliuTeam *obj = [[WliuTeam alloc] initWithWliuTeamDic:dic];
				[resultArr addObject:obj];
			}
			_team = [resultArr copy];
			_xxasdaa = [[infoDic objectForKey:@"xxasdaa"] floatValue];
			_style = [[infoDic objectForKey:@"style"] integerValue];
			_code = [infoDic objectForKey:@"code"];
			_message = [infoDic objectForKey:@"message"];

		}
	}
	return self;
} 

@end


