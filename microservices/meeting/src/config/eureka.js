const { Eureka } = require('eureka-js-client');

module.exports = function registerWithEureka(PORT) {
    const client = new Eureka({
        instance: {
            app: 'MEETING',
            instanceId: `meeting:${PORT}`,          // unique par instance
            hostName: 'localhost',
            ipAddr: '127.0.0.1',
            port: { '$': Number(PORT), '@enabled': true },
            vipAddress: 'meeting',
            statusPageUrl: `http://localhost:${PORT}/info`,
            healthCheckUrl: `http://localhost:${PORT}/health`,
            dataCenterInfo: {
                '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
                name: 'MyOwn',
            },
        },
        eureka: {
            host: '127.0.0.1',
            port: 8761,
            servicePath: '/eureka/apps/',
        },
    });

    client.start((err) => {
        console.log(err ? `Eureka: ${err}` : 'Meeting registered in Eureka');
    });

    const stop = () => client.stop(() => process.exit(0));
    process.on('SIGINT', stop);
    process.on('SIGTERM', stop);
};