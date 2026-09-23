// 切换到指定数据库
db = db.getSiblingDB('douyin_analysis');

// 1. 创建 hot_words 集合并添加索引
db.createCollection("hot_words", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["title", "hot_value", "created_at"],
            properties: {
                position: { bsonType: "int" },
                title: { bsonType: "string" },
                link: { bsonType: "string" },
                time: { bsonType: "string" },
                hot_value: { bsonType: "int" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.hot_words.createIndex({ "created_at": -1 });
db.hot_words.createIndex({ "hot_value": -1 });
db.hot_words.createIndex({ "position": 1 });

// 2. 创建 hot_categories 集合并添加索引
db.createCollection("hot_categories", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["category", "date", "hot_list", "created_at"],
            properties: {
                category: { bsonType: "string" },
                date: { bsonType: "string" },
                hot_list: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["rank", "title", "hot_value"],
                        properties: {
                            rank: { bsonType: "int" },
                            title: { bsonType: "string" },
                            hot_value: { bsonType: "int" }
                        }
                    }
                },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.hot_categories.createIndex({ "category": 1, "date": -1 });
db.hot_categories.createIndex({ "created_at": -1 });

// 3. 创建 daren_rank 集合并添加索引
db.createCollection("daren_rank", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "nickname", "date", "created_at"],
            properties: {
                user_id: { bsonType: "string" },
                nickname: { bsonType: "string" },
                fans: { bsonType: "int" },
                sales: { bsonType: "number" },
                change: { bsonType: "number" },
                date: { bsonType: "string" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.daren_rank.createIndex({ "user_id": 1 });
db.daren_rank.createIndex({ "date": -1 });
db.daren_rank.createIndex({ "sales": -1 });
db.daren_rank.createIndex({ "fans": -1 });

// 4. 创建 hot_videos 集合并添加索引
db.createCollection("hot_videos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["video_id", "user_id", "title", "created_at"],
            properties: {
                video_id: { bsonType: "string" },
                user_id: { bsonType: "string" },
                title: { bsonType: "string" },
                user: { bsonType: "string" },
                date: { bsonType: "string" },
                likes: { bsonType: "string" },
                shares: { bsonType: "string" },
                comments: { bsonType: "string" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.hot_videos.createIndex({ "video_id": 1 });
db.hot_videos.createIndex({ "user_id": 1 });
db.hot_videos.createIndex({ "created_at": -1 });
db.hot_videos.createIndex({ "likes": -1 });

// 5. 创建 user_data 集合并添加索引
db.createCollection("user_data", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "nickname", "created_at"],
            properties: {
                user_id: { bsonType: "string" },
                nickname: { bsonType: "string" },
                fans_count: { bsonType: "int" },
                video_count: { bsonType: "int" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.user_data.createIndex({ "user_id": 1 }, { unique: true });
db.user_data.createIndex({ "fans_count": -1 });
db.user_data.createIndex({ "created_at": -1 });

// 6. 创建 user_stats 集合并添加索引
db.createCollection("user_stats", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "date", "created_at"],
            properties: {
                user_id: { bsonType: "string" },
                date: { bsonType: "string" },
                fans_count: { bsonType: "int" },
                fans_increase: { bsonType: "int" },
                video_count: { bsonType: "int" },
                avg_play: { bsonType: "int" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.user_stats.createIndex({ "user_id": 1, "date": -1 });
db.user_stats.createIndex({ "created_at": -1 });

// 7. 创建 fan_profiles 集合并添加索引
db.createCollection("fan_profiles", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "date", "created_at"],
            properties: {
                user_id: { bsonType: "string" },
                date: { bsonType: "string" },
                gender_ratio: {
                    bsonType: "object",
                    required: ["female", "male"],
                    properties: {
                        female: { bsonType: "number" },
                        male: { bsonType: "number" }
                    }
                },
                age_distribution: { bsonType: "object" },
                location_distribution: { bsonType: "object" },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.fan_profiles.createIndex({ "user_id": 1, "date": -1 });
db.fan_profiles.createIndex({ "created_at": -1 });

// 8. 创建 content_suggestions 集合并添加索引
db.createCollection("content_suggestions", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["date", "created_at"],
            properties: {
                date: { bsonType: "string" },
                hot_topics: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["title", "hot_value"],
                        properties: {
                            title: { bsonType: "string" },
                            hot_value: { bsonType: "int" }
                        }
                    }
                },
                best_time: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["time_range", "effectiveness"],
                        properties: {
                            time_range: { bsonType: "string" },
                            effectiveness: { bsonType: "number" }
                        }
                    }
                },
                recommended_music: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["title", "hot_value"],
                        properties: {
                            title: { bsonType: "string" },
                            hot_value: { bsonType: "int" }
                        }
                    }
                },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.content_suggestions.createIndex({ "date": -1 });
db.content_suggestions.createIndex({ "created_at": -1 });

// 9. 创建 word_cloud 集合并添加索引
db.createCollection("word_cloud", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["date", "words", "created_at"],
            properties: {
                date: { bsonType: "string" },
                words: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["name", "value"],
                        properties: {
                            name: { bsonType: "string" },
                            value: { bsonType: "int" }
                        }
                    }
                },
                created_at: { bsonType: "date" }
            }
        }
    }
});
db.word_cloud.createIndex({ "date": -1 });
db.word_cloud.createIndex({ "created_at": -1 });

// 打印创建完成信息
print("MongoDB collections and indexes created successfully!");