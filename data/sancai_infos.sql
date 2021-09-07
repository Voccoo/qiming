/*
 Navicat Premium Data Transfer

 Source Server         : 云DB
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : dashujuip.f3322.net:53013
 Source Schema         : qiming

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 07/09/2021 14:37:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sancai_infos
-- ----------------------------
DROP TABLE IF EXISTS `sancai_infos`;
CREATE TABLE `sancai_infos`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` int(11) NULL DEFAULT NULL COMMENT '总共81',
  `parse` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '解释',
  `other` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '其他解释',
  `status` int(1) NULL DEFAULT 0 COMMENT ' 1 吉 2 一般 3 凶   0 未分配',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `number`(`number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 163 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sancai_infos
-- ----------------------------
INSERT INTO `sancai_infos` VALUES (82, 1, '（太极之数）太极之数，万物开泰，生发无穷，利禄亨通。（吉）', '情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (83, 2, '（两仪之数）两仪之数，混沌未开，进退保守，志望难达。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (84, 3, '（三才之数）三才之数，天地人和，大事大业，繁荣昌隆。（吉）', '首领、理智发达、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (85, 4, '（四象之数）四象之数，待于生发，万事慎重，不具营谋。（凶）', '孤独、', 3);
INSERT INTO `sancai_infos` VALUES (86, 5, '（五行之数）五行俱全，循环相生，圆通畅达，福祉无穷。（吉）', '女德、(男)双妻、温和、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (87, 6, '（六爻之数）六爻之数，发展变化，天赋美德，吉祥安泰。（吉）', '女德、(男)双妻、温和、', 2);
INSERT INTO `sancai_infos` VALUES (88, 7, '（七政之数）七政之数，精悍严谨，天赋之力，吉星照耀。（吉）', '刚情、意志坚强、', 2);
INSERT INTO `sancai_infos` VALUES (89, 8, '（八卦之数）八卦之数，乾坎艮震，巽离坤兑，无穷无尽。（半吉）', '情感浓厚、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (90, 9, '（大成之数）大成之数，蕴涵凶险，或成或败，难以把握。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (91, 10, '（终结之数）终结之数，雪暗飘零，偶或有成，回顾茫然。（凶）', '孤独、', 3);
INSERT INTO `sancai_infos` VALUES (92, 11, '（旱苗逢雨）万物更新，调顺发达，恢弘泽世，繁荣富贵。（吉）', '女德、温和、情感浓厚、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (93, 12, '（掘井无泉）无理之数，发展薄弱，虽生不足，难酬志向。（凶）', '孤独、', 3);
INSERT INTO `sancai_infos` VALUES (94, 13, '（春日牡丹）才艺多能，智谋奇略，忍柔当事，鸣奏大功。（吉）', '首领、才能、女德、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (95, 14, '（破兆）家庭缘薄，孤独遭难，谋事不达，悲惨不测。（凶）', '才能、孤独、', 3);
INSERT INTO `sancai_infos` VALUES (96, 15, '（福寿）福寿圆满，富贵荣誉，涵养雅量，德高望重。（吉）', '财富、女德、(男)双妻、温和、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (97, 16, '（厚重）厚重载德，安富尊荣，财官双美，功成名就。（吉）', '首领、财富、女德、(男)双妻、温和、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (98, 17, '（刚强）权威显达，突破万难，如能容忍，必获成功。（半吉）', '刚情、意志坚强、', 2);
INSERT INTO `sancai_infos` VALUES (99, 18, '（铁镜重磨）权威显达，博得名利，且养柔德，功成名就。（半吉）', '才能、刚情、意志坚强、', 2);
INSERT INTO `sancai_infos` VALUES (100, 19, '（多难）风云蔽日，辛苦重来，虽有智谋，万事挫折。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (101, 20, '（屋下藏金）非业破运，灾难重重，进退维谷，万事难成。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (102, 21, '（明月中天）风光霁月，万物确立，官运亨通，大博名利。（吉）妇性不宜此数。', '首领、女性孤寡、理智发达、情感浓厚、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (103, 22, '（秋草逢霜）秋草逢霜，困难疾弱，虽出豪杰，人生波折。（凶）', '孤独、', 3);
INSERT INTO `sancai_infos` VALUES (104, 23, '（壮丽）旭日东升，壮丽壮观，权威旺盛，功名荣达。（吉）女性不宜此数。', '首领、女性孤寡、理智发达、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (105, 24, '（掘藏得金）家门余庆，金钱丰盈，白手成家，财源广进。（吉）', '财富、女德、温和、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (106, 25, '（荣俊）资性英敏，才能奇特，克服傲慢，尚可成功。（半吉）', '刚情、理智发达、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (107, 26, '（变怪）变怪之谜，英雄豪杰，波澜重叠，而奏大功。（凶）', '才能、女性孤寡、', 3);
INSERT INTO `sancai_infos` VALUES (108, 27, '（增长）欲望无止，自我强烈，多受毁谤，尚可成功。（半吉）', '刚情、', 2);
INSERT INTO `sancai_infos` VALUES (109, 28, '（阔水浮萍）遭难之数，豪杰气概，四海漂泊，终世浮躁。（凶）女性不宜此数。', '女性孤寡、孤独、刚情、', 3);
INSERT INTO `sancai_infos` VALUES (110, 29, '（智谋）智谋优秀，财力归集，名闻海内，成就大业。（吉）', '首领、财富、才能、女性孤寡、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (111, 30, '（非运）沉浮不定，凶吉难变，若明若暗，大成大败。（半吉）', '', 2);
INSERT INTO `sancai_infos` VALUES (112, 31, '（春日花开）智勇得志，博得名利，统领众人，繁荣富贵。（吉）', '首领、温和、理智发达、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (113, 32, '（宝马金鞍）侥幸多望，贵人得助，财帛如裕，繁荣至上。（吉）', '女德、(男)双妻、温和、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (114, 33, '（旭日升天）旭日升天，鸾凤相会，名闻天下，隆昌至极。（吉）女性不宜此数。', '财富、才能、女性孤寡、理智发达、情感浓厚、', 1);
INSERT INTO `sancai_infos` VALUES (115, 34, '（破家）破家之身，见识短小，辛苦遭逢，灾难至极。（凶）', '孤独、', 3);
INSERT INTO `sancai_infos` VALUES (116, 35, '（高楼望月）温和平静，智达通畅，文吕技艺，奏功洋洋。（吉）', '才能、女德、温和、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (117, 36, '（波澜重叠）波澜重叠，沉浮万状，侠肝义胆，舍已成仁。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (118, 37, '（猛虎出林）权威显达，热诚忠信，宜着雅量，终身荣富。（吉）', '首领、刚情、理智发达、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (119, 38, '（磨铁成针）意志薄弱，刻意经营，才识不凡，技艺有成。（吉）', '才能、', 1);
INSERT INTO `sancai_infos` VALUES (120, 39, '（富贵荣华）富贵荣华，财帛丰盈，暗藏险象，德泽四方。（半吉）', '首领、女性孤寡、(男)双妻、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (121, 40, '（退安）智谋胆力，冒险投机，沉浮不定，退保平安。（半吉）', '', 2);
INSERT INTO `sancai_infos` VALUES (122, 41, '（有德）纯阳独秀，德高望重，和顺畅达，博得名利。（大吉）此数为最大好运数。', '首领、财富、(男)双妻、理智发达、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (123, 42, '（寒蝉在柳）博识多能，精通世情，如能专心，尚可成功。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (124, 43, '（散财破产）散财破产，诸事不遂，虽有智谋，财来财去。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (125, 44, '（烦闷）破家亡身，暗藏惨淡，事不如意，乱世怪杰。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (126, 45, '（顺风）新生泰和，顺风扬帆，智谋经纬，富贵繁荣。（吉）', '首领、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (127, 46, '（浪里陶金）载宝沉舟，浪里陶金，大难尝尽，大功有成。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (128, 47, '（点石成金）花开之象，万事如意，祯祥吉庆，天赋幸福。（吉）', '首领、刚情、意志坚强、', 1);
INSERT INTO `sancai_infos` VALUES (129, 48, '（古松立鹤）智谋兼备，德量荣达，威望成师，洋洋大观。（吉）', '才能、理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (130, 49, '（转变）吉临则吉，凶来则凶，转凶为吉，配好三才。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (131, 50, '（小舟入海）一成一败，吉凶参半，先得庇荫，后遭凄惨。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (132, 51, '（沉浮）盛衰交加，波澜重叠，如能慎始，必获成功。（半吉）', '', 2);
INSERT INTO `sancai_infos` VALUES (133, 52, '（达眼）卓识达眼，先见之明，智谋超群，名利双收。（吉）', '', 1);
INSERT INTO `sancai_infos` VALUES (134, 53, '（曲卷难星）外祥内崽，外祸内安，先富后贫，先贫后富。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (135, 54, '（石上栽花）石上栽花，难得有活，忧闷烦来，辛惨不绝。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (136, 55, '（善恶）善善得恶，恶恶得善，吉到极限，反生凶险。（半吉）', '', 2);
INSERT INTO `sancai_infos` VALUES (137, 56, '（浪里行舟）历尽艰辛，四周障碍，万事龌龊，做事难成。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (138, 57, '（日照春松）寒雪青松，夜莺吟春，必遭一过，繁荣白事。（吉）', '', 1);
INSERT INTO `sancai_infos` VALUES (139, 58, '（晚行遇月）沉浮多端，先苦后甜，宽宏扬名，富贵繁荣。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (140, 59, '（寒蝉悲风）寒蝉悲风，意志衰退，缺乏忍耐，苦难不休。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (141, 60, '（无谋）无谋之人，漂泊不定，晦暝暗黑，动摇不安。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (142, 61, '（牡丹芙蓉）牡丹芙蓉，花开富贵，名利双收，定享天赋。（吉）', '', 2);
INSERT INTO `sancai_infos` VALUES (143, 62, '（衰败）衰败之象，内外不和，志望难达，灾祸频来。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (144, 63, '（舟归平海）富贵荣华，身心安泰，雨露惠泽，万事亨通。（吉）', '理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (145, 64, '（非命）骨肉分离，孤独悲愁，难得安心，做事不成。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (146, 65, '（巨流归海）天长地久，家运隆昌，福寿绵长，事事成就。（吉）', '', 1);
INSERT INTO `sancai_infos` VALUES (147, 66, '（岩头步马）进退维谷，难舍不堪，等待时机，一跃而起。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (148, 67, '（顺风通达）天赋幸运，四通八达，家道繁昌，富贵东来。（吉）', '理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (149, 68, '（顺风吹帆）智虑周密，集众信达，发明能智，拓展昴进。（吉）', '理智发达、', 1);
INSERT INTO `sancai_infos` VALUES (150, 69, '（非业）非业非力，精神迫滞，灾害交至，遍偿痛苦。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (151, 70, '（残菊逢霜）残菊逢霜，寂寞无碍，惨淡忧愁，晚景凄凉。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (152, 71, '（石上金花）石上金花，内心劳苦，贯彻始终，定可昌隆。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (153, 72, '（劳苦）荣苦相伴，阴云覆月，外表吉祥，内实凶祸。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (154, 73, '（无勇）盛衰交加，徒有高志，天王福祉，终世平安。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (155, 74, '（残菊经霜）残菊经霜，秋叶寂寞，无能无智，辛苦繁多。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (156, 75, '（退守）退守保吉，发迹甚迟，虽有吉象，无谋难成。（凶）', '', 2);
INSERT INTO `sancai_infos` VALUES (157, 76, '（离散）倾覆离散，骨肉分离，内外不和，虽劳无功。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (158, 77, '（半吉）家庭有悦，半吉半凶，能获援护，陷落不幸。（半吉）', '', 3);
INSERT INTO `sancai_infos` VALUES (159, 78, '（晚苦）祸福参半，先天智能，中年发达，晚景困苦。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (160, 79, '（云头望月）云头望月，身疲力尽，穷追不伸，精神不定。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (161, 80, '（遁吉）辛苦不绝，早入隐遁，安心立命，化凶转吉。（凶）', '', 3);
INSERT INTO `sancai_infos` VALUES (162, 81, '（万物回春）最吉之数，还本归元，吉祥重叠，富贵尊荣。（大吉）', '', 1);

SET FOREIGN_KEY_CHECKS = 1;
