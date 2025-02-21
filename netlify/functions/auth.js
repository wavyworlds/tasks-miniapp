const crypto = require("crypto");

exports.handler = async (event) => {
    const BOT_TOKEN = process.env.BOT_TOKEN;
    const userData = JSON.parse(event.body);

    function verifyTelegramLogin(data) {
        const secret = crypto.createHmac("sha256", BOT_TOKEN).update("WebAppData").digest();
        const checkString = Object.keys(data)
            .filter((key) => key !== "hash")
            .map((key) => `${key}=${data[key]}`)
            .sort()
            .join("\n");

        const hash = crypto.createHmac("sha256", secret).update(checkString).digest("hex");
        return hash === data.hash;
    }

    if (verifyTelegramLogin(userData)) {
        return {
            statusCode: 200,
            body: JSON.stringify({ success: true, user: userData }),
        };
    } else {
        return {
            statusCode: 403,
            body: JSON.stringify({ success: false, message: "Unauthorized" }),
        };
    }
};
