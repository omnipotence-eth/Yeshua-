"""
Configuration file for the X AI Agent Bible Verse Bot
"""

# API Usage Limits (X Free Tier)
API_LIMITS = {
    'monthly_posts': 500,  # 500 posts per month
    'monthly_reads': 100,  # 100 read requests per month
    'daily_posts': 17,     # ~17 posts per day (500/30)
    'daily_reads': 4,      # ~4 reads per day (100/30)
    'posts_per_thread': 2  # Each verse thread = 2 posts
}

# Target accounts for interactions (crypto/finance influencers)
TARGET_ACCOUNTS = {
    # Crypto accounts
    'VitalikButerin': '295218901',
    'saylor': '244647486', 
    'cz_binance': '98945122',
    'elonmusk': '44196397',
    'naval': '17874544',
    
    # Finance accounts
    'MarketWatch': '624413',
    'WSJ': '3108351',
    'bloomberg': '34713362',
    'Reuters': '1652541',
    'FT': '18949452'
}

# Chinese book name mapping for bible-api.com
CHINESE_BOOK_MAP = {
    'genesis': '创世记',
    'exodus': '出埃及记',
    'leviticus': '利未记',
    'numbers': '民数记',
    'deuteronomy': '申命记',
    'joshua': '约书亚记',
    'judges': '士师记',
    'ruth': '路得记',
    '1samuel': '撒母耳记上',
    '2samuel': '撒母耳记下',
    '1kings': '列王纪上',
    '2kings': '列王纪下',
    '1chronicles': '历代志上',
    '2chronicles': '历代志下',
    'ezra': '以斯拉记',
    'nehemiah': '尼希米记',
    'esther': '以斯帖记',
    'job': '约伯记',
    'psalms': '诗篇',
    'psalm': '诗篇',
    'proverbs': '箴言',
    'ecclesiastes': '传道书',
    'songofsolomon': '雅歌',
    'isaiah': '以赛亚书',
    'jeremiah': '耶利米书',
    'lamentations': '耶利米哀歌',
    'ezekiel': '以西结书',
    'daniel': '但以理书',
    'hosea': '何西阿书',
    'joel': '约珥书',
    'amos': '阿摩司书',
    'obadiah': '俄巴底亚书',
    'jonah': '约拿书',
    'micah': '弥迦书',
    'nahum': '那鸿书',
    'habakkuk': '哈巴谷书',
    'zephaniah': '西番雅书',
    'haggai': '哈该书',
    'zechariah': '撒迦利亚书',
    'malachi': '玛拉基书',
    'matthew': '马太福音',
    'mark': '马可福音',
    'luke': '路加福音',
    'john': '约翰福音',
    'acts': '使徒行传',
    'romans': '罗马书',
    '1corinthians': '哥林多前书',
    '2corinthians': '哥林多后书',
    'galatians': '加拉太书',
    'ephesians': '以弗所书',
    'philippians': '腓立比书',
    'colossians': '歌罗西书',
    '1thessalonians': '帖撒罗尼迦前书',
    '2thessalonians': '帖撒罗尼迦后书',
    '1timothy': '提摩太前书',
    '2timothy': '提摩太后书',
    'titus': '提多书',
    'philemon': '腓利门书',
    'hebrews': '希伯来书',
    'james': '雅各书',
    '1peter': '彼得前书',
    '2peter': '彼得后书',
    '1john': '约翰一书',
    '2john': '约翰二书',
    '3john': '约翰三书',
    'jude': '犹大书',
    'revelation': '启示录'
}

# Daily themes for verse selection
DAILY_THEMES = {
    'monday': 'hope',
    'tuesday': 'wisdom', 
    'wednesday': 'perseverance',
    'thursday': 'faith',
    'friday': 'love',
    'saturday': 'peace',
    'sunday': 'gratitude'
}

# Theme-based verse suggestions for AI (expanded for variety)
THEME_VERSE_SUGGESTIONS = {
    'hope': [
        'Romans 15:13', 'Jeremiah 29:11', 'Psalm 27:14', 'Isaiah 40:31',
        'Lamentations 3:22-23', 'Romans 8:28', 'Psalm 31:24', 'Isaiah 41:10',
        'Romans 12:12', 'Psalm 62:5', '1 Corinthians 13:13', 'Psalm 33:18',
        'Isaiah 25:9', 'Romans 5:5', 'Titus 2:13', '1 Timothy 4:10',
        'Psalm 71:14', 'Isaiah 26:3', 'Romans 15:4', 'Hebrews 6:19'
    ],
    'wisdom': [
        'Proverbs 3:5-6', 'James 1:5', 'Proverbs 16:16', 'Proverbs 9:10',
        'Psalm 111:10', 'Proverbs 2:6', 'Colossians 2:3', '1 Corinthians 1:25',
        'Proverbs 4:7', 'Ecclesiastes 7:12', 'Job 28:28', 'Proverbs 1:7',
        'Psalm 19:7', 'Proverbs 8:11', 'Daniel 2:20', 'Proverbs 3:13',
        'Ecclesiastes 2:26', 'Proverbs 24:3-4', 'James 3:17', 'Proverbs 19:8'
    ],
    'perseverance': [
        'Romans 5:3-4', 'Hebrews 12:1', 'Galatians 6:9', 'James 1:12',
        '2 Timothy 4:7-8', '1 Corinthians 9:24', 'Philippians 3:14', 'Hebrews 10:36',
        'Romans 8:25', '1 Thessalonians 1:3', '2 Thessalonians 3:13', 'Revelation 2:3',
        'Matthew 24:13', 'Luke 21:19', 'Acts 14:22', 'Romans 2:7',
        'Colossians 1:11', '2 Timothy 2:12', 'Hebrews 6:15', 'James 5:11'
    ],
    'faith': [
        'Hebrews 11:1', 'Mark 11:22', '2 Corinthians 5:7', 'Romans 10:17',
        'Galatians 2:20', 'Ephesians 2:8', 'James 2:17', '1 Peter 1:8-9',
        'John 3:16', 'Matthew 17:20', 'Mark 9:23', 'Luke 17:6',
        'Romans 4:20-21', 'Hebrews 11:6', '1 John 5:4', 'Revelation 2:10',
        'Matthew 21:21', 'Mark 11:22-24', 'Luke 18:8', 'John 14:1'
    ],
    'love': [
        '1 Corinthians 13:4-7', 'John 3:16', 'Romans 8:38-39', '1 John 4:19',
        'Ephesians 5:25', 'Song of Solomon 8:7', '1 Peter 4:8', 'Proverbs 10:12',
        '1 John 3:16', 'Romans 13:10', 'Galatians 5:22-23', '1 Corinthians 16:14',
        'Colossians 3:14', '1 John 4:7-8', 'Matthew 22:37-39', 'John 13:34-35',
        '1 John 4:16', 'Romans 5:8', 'Ephesians 3:17-19', '1 Corinthians 13:13'
    ],
    'peace': [
        'Philippians 4:7', 'John 14:27', 'Isaiah 26:3', 'Romans 5:1',
        'Colossians 3:15', 'Psalm 29:11', 'Isaiah 9:6', 'Matthew 5:9',
        'Romans 8:6', 'Galatians 5:22', 'Ephesians 2:14', '2 Thessalonians 3:16',
        'Psalm 4:8', 'Isaiah 32:17', 'John 16:33', 'Psalm 85:8',
        'Isaiah 54:10', 'Romans 14:17', 'Philippians 4:9', 'Colossians 1:20'
    ],
    'gratitude': [
        '1 Thessalonians 5:18', 'Psalm 100:4', 'Colossians 3:17', 'Ephesians 5:20',
        'Psalm 107:1', 'Psalm 118:1', 'Psalm 136:1', '2 Corinthians 9:15',
        'Psalm 95:2', 'Psalm 96:2', 'Psalm 98:1', 'Psalm 105:1',
        'Psalm 106:1', 'Psalm 111:1', 'Psalm 112:1', 'Psalm 113:1',
        'Psalm 117:1', 'Psalm 135:1', 'Psalm 138:1', 'Psalm 139:14'
    ],
    'strength': [
        'Philippians 4:13', 'Isaiah 40:31', 'Psalm 18:2', '2 Corinthians 12:9',
        'Ephesians 6:10', 'Psalm 27:1', 'Isaiah 41:10', 'Deuteronomy 31:6',
        'Joshua 1:9', 'Psalm 46:1', 'Isaiah 12:2', 'Nahum 1:7',
        'Psalm 28:7', '2 Samuel 22:33', 'Psalm 18:32', 'Exodus 15:2',
        'Psalm 59:17', 'Isaiah 25:4', '2 Chronicles 20:15', 'Psalm 29:11'
    ],
    'joy': [
        'Nehemiah 8:10', 'Psalm 16:11', 'Galatians 5:22', 'Philippians 4:4',
        '1 Thessalonians 5:16', 'Psalm 30:5', 'Isaiah 12:3', 'Luke 2:10',
        'Acts 13:52', 'Romans 15:13', '1 Peter 1:8', 'Psalm 28:7',
        'Habakkuk 3:18', 'John 15:11', 'Psalm 97:11', 'Psalm 126:3',
        'Isaiah 35:10', 'Luke 15:7', 'Acts 8:8', 'Romans 14:17'
    ],
    'grace': [
        'Ephesians 2:8-9', 'Romans 3:23-24', '2 Corinthians 12:9', 'Titus 2:11',
        'Romans 5:20', 'Ephesians 1:7', 'Romans 6:14', '2 Corinthians 9:8',
        'Hebrews 4:16', 'James 4:6', '1 Peter 5:10', 'John 1:16-17',
        'Romans 11:6', 'Galatians 2:21', 'Ephesians 2:5', 'Colossians 1:6',
        '2 Timothy 1:9', 'Titus 3:7', 'Hebrews 13:9', '1 Peter 1:13'
    ],
    'market_crash': [
        'Matthew 6:19-21', 'Proverbs 23:4-5', 'Luke 12:15', 'Ecclesiastes 5:10',
        '1 Timothy 6:9-10', 'Proverbs 11:28', 'Matthew 6:24', 'Luke 16:13',
        'Proverbs 13:11', 'Proverbs 22:7', 'Ecclesiastes 2:18-19', 'Psalm 49:6-7',
        'Proverbs 15:16', 'Proverbs 16:8', 'Proverbs 28:20', 'Ecclesiastes 4:6',
        'Matthew 19:24', 'Mark 10:25', 'Luke 18:25', '1 Timothy 6:17'
    ],
    'crypto': [
        'Proverbs 13:11', 'Luke 16:11', 'Matthew 25:14-30', 'Proverbs 21:5',
        'Proverbs 24:3-4', 'Ecclesiastes 11:2', 'Proverbs 27:23-24', 'Luke 14:28-30',
        'Proverbs 6:6-8', 'Proverbs 10:4', 'Proverbs 12:11', 'Proverbs 14:23',
        'Proverbs 20:4', 'Proverbs 21:20', 'Proverbs 22:3', 'Proverbs 24:27',
        'Proverbs 28:19', 'Ecclesiastes 5:13', 'Luke 19:12-26', 'Matthew 6:33'
    ],
    'finance': [
        'Proverbs 22:7', '1 Timothy 6:10', 'Malachi 3:10', 'Proverbs 3:9-10',
        'Proverbs 11:24-25', '2 Corinthians 9:6-7', 'Luke 6:38', 'Proverbs 19:17',
        'Proverbs 28:27', 'Deuteronomy 15:10', 'Proverbs 14:31', 'Proverbs 21:13',
        'Proverbs 22:9', 'Proverbs 28:8', 'Ecclesiastes 11:1', 'Proverbs 13:22',
        'Proverbs 19:4', 'Proverbs 21:20', 'Proverbs 22:16', 'Proverbs 28:20'
    ]
}
