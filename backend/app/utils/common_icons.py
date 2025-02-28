# Define event icons
event_icons = {
    # Payment-related events
    "payment.authorized": "🟢💳",
    "payment.failed": "🔴❌",
    "payment.captured": "🟢✅",
    "payment.downtime.started": "⏳🔻",
    "payment.downtime.updated": "🔄🔁",
    "payment.downtime.resolved": "✔️🔼",

    # Order-related events
    "order.paid": "💰✅",
    "order.notification.delivered": "📤📨",
    "order.notification.failed": "📭❌",

    # Invoice-related events
    "invoice.paid": "🧾✅",
    "invoice.partially_paid": "🧾🔸",
    "invoice.expired": "🧾⏳",

    # Subscription-related events
    "subscription.authenticated": "🔑🆗",
    "subscription.paused": "⏸️🛑",
    "subscription.resumed": "▶️🔄",
    "subscription.activated": "⚡🔥",
    "subscription.pending": "⏳⌛",
    "subscription.halted": "❌⛔",
    "subscription.charged": "💸💳",
    "subscription.cancelled": "❌🚫",
    "subscription.completed": "✔️🏁",
    "subscription.updated": "🔄⚙️",

    # Settlement-related events
    "settlement.processed": "💵📥",

    # Virtual account-related events
    "virtual_account.credited": "💰➕",
    "virtual_account.created": "🎉🆕",
    "virtual_account.closed": "🔒🔚",

    # QR Code-related events
    "qr_code.closed": "🔒❌",
    "qr_code.created": "🔑🆕",
    "qr_code.credited": "💸📸",

    # Fund account validation
    "fund_account.validation.completed": "✅🔍",
    "fund_account.validation.failed": "❌⚠️",

    # Refund-related events
    "refund.speed_changed": "⚡🔄",
    "refund.processed": "💸📤",
    "refund.failed": "❌📉",
    "refund.created": "📝💵",

    # Transfer-related events
    "transfer.processed": "💸🔄",
    "transfer.failed": "❌💰",

    # Account-related events
    "account.instantly_activated": "⚡🆕",
    "account.activated_kyc_pending": "📝⏳",
    "account.under_review": "🔍🧐",
    "account.needs_clarification": "❓🤔",
    "account.activated": "✅🆗",
    "account.rejected": "❌🚷",
    "account.updated": "🔄📜",

    # Payment link-related events
    "payment_link.paid": "💰🔗",
    "payment_link.partially_paid": "🔸💰",
    "payment_link.expired": "⏳🔗",
    "payment_link.cancelled": "❌🔗",

    # Product route-related events
    "product.route.under_review": "🔍🛤️",
    "product.route.activated": "✅🚀",
    "product.route.needs_clarification": "❓💬",
    "product.route.rejected": "❌🚫",

    # API routes and endpoints
    "openapi.json": "📜🔍",
    "swagger_ui_html": "📝📖",
    "swagger_ui_redirect": "🔄➡️",
    "redoc_html": "📄📚",
    "index": "🏠📍",
    "register": "📝🆕",
    "otpVerify": "🔑✔️",
    "user.get": "👤📂",
    "user.update": "✏️🔄",
    "user.delete": "🗑️🚮",
    "choose_ticket": "🎟️✔️",
    
    # Websocket-related events
    "websocket_general_endpoint": "🌐📡",
    "websocket_realtime_endpoint": "📡⏳",
    "websocket_otp_status_endpoint": "🔑🕵️",
    "websocket_session_endpoint": "💬🔗",

    # User-related events
    "user.signup": "👤🆕",
    "user.logged_in": "🔑👤",
    "user.logged_out": "🚪👋",
    "user.deleted": "🗑️❌",
    "user.suspended": "⛔🚫",

    # System-related events
    "system.error": "⚠️💥",
    "system.maintenance": "🛠️🔧",
    "system.reboot": "🔄🔌",

    # Notification events
    "notification.new": "🔔🆕",
    "notification.read": "✅📩",
    "notification.deleted": "🗑️🔕",

    # Miscellaneous
    "password.show": "👁️",
    "password.hide": "👁️",
    "registration.form": "📝",
    "form.loading": "⏳",
    "forword.route": "➡️ ",
    "back.route": "⬅️ ",
    "calculating.time": "⏳",
    "check": "✅🔍",
    "check.passed": "✅",
    "check.failed": "❌",
    "warning": "⚠️",
    "success": "✅",
    "info": "ℹ️",
    "search": "🔍🧐",
    "help": "❓",
    "settings": "⚙️🔧",
    "refresh": "🔄♻️",
    "update": "🔄📢",
    "upload": "⬆️📤",
    "download": "⬇️📥",
    "lock": "🔒🔐",
    "unlock": "🔓🛠️",
    "share": "🔗📨",
    "home": "🏠🛖",
    "calendar": "📅🗓️",
    "message": "📩✉️",
    "phone": "📱📞",
    "email": "📧📨",
    "location": "📍🗺️",
    "bell": "🔔⏰",
    "success": "✅🎉",
    "error": "⚠️❗",
    "warning": "⚠️⚡",
    "info": "ℹ️💡",
    "question": "❓🤔",
    "completed": "✔️🎯",
    "failed": "❌📉",
    "new": "🆕✨",
    "edit": "✏️📝",
    "delete": "🗑️🛑",
    "pause": "⏸️⏳",
    "play": "▶️🎬",
    "stop": "⏹️🚫",
    "star": "⭐🌟",
    "fire": "🔥💥",
    "thumb_up": "👍✅",
    "thumb_down": "👎❌",
    "pencil": "✏️🖊️",
    "check_mark": "✔️✅",
    "cross": "❌❎",
    "comment": "💬🗣️",
    "handshake": "🤝💼",
    
    # Database operations

    "database": "🐘",
    "database.connecting": "🔌❎🐘",
    "database.connected": "🔌🐘",
    "database.disconnected": "❌🐘",
    "database.warning": "⚠️🐘",
    "database.error": "❌🐘",
    "database.create": "🗃️🆕",
    "database.delete": "🗑️🗄️",
    "database.update": "🔄📊",
    "database.get": "📂🔎",
    "database.list": "📂📋",
    
    # RabbitMQ operations
    "rabbitmq": "🐰📡",
    "rabbitmq.connecting": "🔌❎🐰📡",
    "rabbitmq.connected": "🔌🐰📡",
    "rabbitmq.disconnected": "❌🐰📡",

    "rabbitmq.queue.create": "🗃️📦",
    "rabbitmq.queue.delete": "🗑️📦",
    "rabbitmq.queue.update": "🔄📦",
    
    # Redis operations
    "redis": "🔴🗄️",
    "redis.connecting": "🔌❎🔴🗄️",
    "redis.connected": "🔌🔴🗄️",
    "redis.disconnected": "❌🔴🗄️",
    "redis.key.create": "🗃️🔑",
    "redis.key.delete": "🗑️🔑",
    "redis.key.update": "🔄🔑",
    "redis.list.create": "🗃️📜",
    "redis.hash.create": "🗃️#️⃣",
    "redis.set.create": "🗃️🔢",
}
