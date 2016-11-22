/*!
 *	producted by oc_json_plugin.py
 *	auth: w6
*/
#import <Foundation/Foundation.h>

@interface WliuTeam : NSObject

@property (nonatomic, assign) NSInteger count;

@property (nonnull, nonatomic, copy) NSString *name;

- (_Nonnull instancetype)initWithWliuTeamDic:(NSDictionary * _Nonnull)infoDic;

@end

@interface WliuResult : NSObject

@property (nonnull, nonatomic, copy) NSString *url;

@property (nonnull, nonatomic, copy) NSString *content;

@property (nonnull, nonatomic, copy) NSString *version;

@property (nonatomic, assign) float filesize;

@property (nonatomic, assign) NSInteger isforce;

- (_Nonnull instancetype)initWithWliuResultDic:(NSDictionary * _Nonnull)infoDic;

@end

@interface WliuBaseModel : NSObject

@property (nonnull, nonatomic, strong) WliuResult *result;

@property (nonnull, nonatomic, strong) NSArray<WliuTeam *> *team;

@property (nonatomic, assign) float xxasdaa;

@property (nonatomic, assign) NSInteger style;

@property (nonnull, nonatomic, copy) NSString *code;

@property (nonnull, nonatomic, copy) NSString *message;

- (_Nonnull instancetype)initWithWliuBaseModelDic:(NSDictionary * _Nonnull)infoDic;

@end
