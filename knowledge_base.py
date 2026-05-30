
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from config import settings

class KnowledgeBaseService:
    """城市文化知识库服务"""

    def __init__(self):
        self.kb_path = settings.KNOWLEDGE_BASE_PATH
        self._init_kb()

    def _init_kb(self):
        """初始化知识库目录和示例数据"""
        # 确保知识库目录存在
        Path(self.kb_path).mkdir(parents=True, exist_ok=True)

        # 如果知识库为空，添加示例数据
        if not any(Path(self.kb_path).iterdir()):
            self._add_sample_data()

    def _add_sample_data(self):
        """添加示例知识库数据"""
        # 北京胡同文化
        self.add_knowledge(
            title="北京胡同里的槐树文化",
            content="北京胡同里的槐树是老北京记忆的一部分。槐树在北京有着悠久的历史，早在元代，槐树就被广泛种植于胡同中。槐花盛开时，满街飘香，是北京夏季特有的味道。槐树树冠茂密，为胡同提供了天然的遮阳伞，使胡同在炎热的夏季也能保持凉爽。槐树还被视为吉祥的象征，'槐'与'怀'谐音，寓意怀念和思乡。在北京的胡同里漫步，常常可以看到百年以上的老槐树，它们见证了胡同的变迁，承载着老北京人的记忆。"
        )

        # 秋季赏桂地图
        self.add_knowledge(
            title="北京秋季赏桂地图",
            content="北京赏桂的最佳季节是9月至10月。颐和园的桂花是北京最著名的，园内有金桂、银桂、丹桂等多个品种，香气浓郁。香山公园的桂花园也是赏桂的好去处，园内种植了大量桂花树，每到秋季，满园飘香。北海公园的琼华岛上也有不少桂花树，登岛赏桂别有一番风味。此外，中山公园、天坛公园、北京植物园等地方也有桂花可供观赏。赏桂的最佳时间是早晨或傍晚，此时气温适中，桂花香气最为浓郁。"
        )

        # 五道营胡同
        self.add_knowledge(
            title="五道营胡同的历史与变迁",
            content="五道营胡同位于北京市东城区，北起雍和宫大街，南至国子监街，全长约632米。明朝时，这里曾是武官驻扎的地方，因此被称为'武德卫营'。清朝时，这里逐渐演变为平民居住区，胡同里的小院落错落有致，充满了老北京的生活气息。近年来，五道营胡同经历了文艺复兴，成为北京最具文艺气息的胡同之一。胡同里聚集了许多特色咖啡馆、书店和手工艺品店，吸引了大量年轻人和文艺爱好者。尽管如此，五道营胡同仍然保留着老北京的风貌，胡同里的老槐树、青砖灰瓦和四合院，让人感受到历史的厚重。"
        )

        # 南锣鼓巷
        self.add_knowledge(
            title="南锣鼓巷的历史典故",
            content="南锣鼓巷是北京最古老的街区之一，始建于元朝，至今已有700多年的历史。南锣鼓巷南北走向，长约800米，东西各有8条胡同整齐排列，呈'鱼骨状'，因此被称为'蜈蚣巷'。南锣鼓巷曾是元大都的市中心，明清时期则是达官显贵的聚居地。胡同里保存着许多名人故居，如清代大将军僧格林沁的府邸、著名画家齐白石的故居等。近年来，南锣鼓巷成为北京最热门的旅游景点之一，胡同里布满了特色小店、咖啡馆和餐馆。尽管商业化程度较高，南锣鼓巷仍然保留着老北京的风貌，是体验北京胡同文化的绝佳去处。"
        )

        # 什刹海
        self.add_knowledge(
            title="什刹海的四季风光",
            content="什刹海由前海、后海和西海三个湖泊组成，是北京城内唯一一处具有开阔水面的开放型景区，被誉为'北方的水乡'。什刹海的四季各有特色：春天，湖边的柳树抽出新芽，湖面上漂浮着点点浮萍；夏天，荷花盛开，湖上泛舟是消暑的好方式；秋天，湖边的银杏树变成金黄色，倒映在湖水中，美不胜收；冬天，湖面结冰，成为天然滑冰场，吸引着众多滑冰爱好者。什刹海周边有许多历史建筑，如恭王府、醇亲王府、宋庆龄故居等，是体验北京历史文化的绝佳地点。此外，什刹海周边还有许多特色酒吧和餐馆，夜晚的什刹海别有一番风情。"
        )

        # 北新桥头条胡同
        self.add_knowledge(
            title="北新桥头条胡同的历史与特色",
            content="北新桥头条胡同位于北京市东城区，东起东直门内大街，西至北新桥大街，全长约300米。据史料记载，元代这里曾是漕运码头，是京杭大运河的重要节点，商贾云集，繁华一时。明代时，这里逐渐演变为居民区，胡同里的四合院错落有致，充满了老北京的生活气息。北新桥头条胡同保留了许多老北京的传统元素，如青砖灰瓦的四合院、门前的石狮子、墙上的砖雕等。胡同里还有一些特色小店，如传统手工艺品店、老北京小吃店等，是体验老北京文化的好去处。"
        )

    def add_knowledge(self, title: str, content: str, tags: List[str] = None) -> str:
        """添加知识条目"""
        if tags is None:
            tags = []

        knowledge_id = f"{title}_{len(os.listdir(self.kb_path))}"

        knowledge_data = {
            "id": knowledge_id,
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": str(Path().stat().st_mtime)
        }

        file_path = os.path.join(self.kb_path, f"{knowledge_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_data, f, ensure_ascii=False, indent=2)

        return knowledge_id

    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """搜索知识库"""
        results = []

        # 简单的关键词匹配，实际应用中可以使用向量搜索或更高级的搜索算法
        query_lower = query.lower()

        for file_path in Path(self.kb_path).glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    knowledge = json.load(f)

                # 计算匹配度
                score = 0
                title_lower = knowledge.get("title", "").lower()
                content_lower = knowledge.get("content", "").lower()
                tags = [tag.lower() for tag in knowledge.get("tags", [])]

                # 标题匹配权重最高
                if query_lower in title_lower:
                    score += 10

                # 内容匹配
                if query_lower in content_lower:
                    score += 5

                # 标签匹配
                for tag in tags:
                    if query_lower in tag:
                        score += 3

                if score > 0:
                    results.append({
                        "id": knowledge.get("id", ""),
                        "title": knowledge.get("title", ""),
                        "content": knowledge.get("content", ""),
                        "tags": knowledge.get("tags", []),
                        "score": score
                    })
            except Exception as e:
                print(f"Error reading knowledge file {file_path}: {e}")

        # 按匹配度排序并返回前N条结果
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_knowledge_by_id(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取知识条目"""
        file_path = os.path.join(self.kb_path, f"{knowledge_id}.json")

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading knowledge file {file_path}: {e}")
            return None

    def get_related_knowledge(self, location: str, lat: float, lon: float) -> List[str]:
        """根据位置获取相关知识"""
        # 首先尝试直接搜索位置名称
        results = self.search_knowledge(location, limit=3)

        # 如果没有找到足够的结果，尝试搜索区域关键词
        if len(results) < 3:
            # 这里可以添加更复杂的地理位置分析，例如根据坐标判断所在区域
            # 目前简单地添加一些通用关键词进行搜索
            general_keywords = ["胡同", "公园", "文化", "历史"]

            for keyword in general_keywords:
                additional_results = self.search_knowledge(keyword, limit=2)
                results.extend(additional_results)

        # 去重并返回
        unique_results = []
        seen_ids = set()

        for result in results:
            if result and result.get("id") not in seen_ids:
                unique_results.append(result.get("content", ""))
                seen_ids.add(result.get("id", ""))

        return unique_results
