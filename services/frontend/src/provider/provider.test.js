import fetchMock from 'fetch-mock';

import providerBase from './base';
import {tokenAuth, globalErrorHandler} from './middlewares';
import {ANALYSIS_LIST, TAXONOMY_TREE} from './test_data';


describe('Test provider Base', () => {
    beforeEach(() => {
        providerBase.setGlobalConfig({base_url: 'http://example.com'});
        providerBase.setMiddlewares([]);

        fetchMock.restore();
    });

    it('Is very basic example', async () => {
        fetchMock.get('http://example.com/v1/data', {
            body: {'field': 'value'},
            status: 200
        });

        const response = await providerBase.get('/v1/data');

        expect(response.field).toBe('value');
    });

    it('Checks if POST / PUT requests are working correctly', async () => {
        fetchMock
            .post((url, {headers, body}) => {
                return url === 'http://example.com/v1/data'
                    && headers['Content-Type'] === 'application/json'
                    && body['some'] === 'data';
            }, {
                body: {'response': 'ok'}
            });

        const response = await providerBase.post('/v1/data', {'some': 'data'});

        expect(response.response).toBe('ok');
    });

    it('Checks if options propagation works', async () => {
        fetchMock
            .put((url, {headers,}) => {
                return url === 'http://example.com/v1/data'
                    && headers['Content-Type'] === 'application/json'
                    && headers['X-Propagated'] === 'test';
            }, {
                body: {'response': 'ok'}
            });

        const response = await providerBase.put('/v1/data', {}, { headers: {'X-Propagated': 'test'}});

        expect(response.response).toBe('ok');
    });

    it('Checks if middlewares works as expected', async () => {
        let testApiKey = 'test';

        fetchMock.get(
            (url, {headers}) => {
                return url === 'http://example.com/v1/data'
                    && headers['X-Api-Key'] === testApiKey
                    && headers['X-Header'] === 'test';
            }, {
                body: {'it': 'works'},
                status: 200
            }
        );

        const testMiddleware = (url, options) => async next => next(url, {
            ...options,
            headers : {
                ...options.headers,
                'X-Header': 'test'
            }
        });

        providerBase.setMiddlewares([
            testMiddleware,
            tokenAuth(testApiKey),
        ]);

        const response = await providerBase.get('/v1/data');

        expect(response.it).toBe('works');
    });

    it('Checks global error handler', async () => {
        fetchMock.get('http://example.com/v1/data', {
            body: {'error': 'message'},
            status: 400
        });
        expect.assertions(1);

        providerBase.setMiddlewares([
            globalErrorHandler((response) => {
                expect(response.status).toBe(400);
            })
        ]);

        const response = await providerBase.get('/v1/data');
    });

    it('Check custom reader function', async () => {
        fetchMock.get(
            'http://example.com/v1/data',
            {
                body: {
                    files: [
                        {id: 1},
                        {id: 2},
                    ]
                },
                status: 200
            });

        const listOfFiles = await providerBase.get('/v1/data', {}, ({files}) => files);

        expect(listOfFiles[0].id).toBe(1);
        expect(listOfFiles[1].id).toBe(2);
    });

    it('Test query params work as expected', async () => {
        fetchMock.get('http://example.com/v1/data?param=test', {
            body: {
                data: 'value'
            }
        });

        const response = await providerBase.get('/v1/data', { query: { param: 'test' } });
    });

    it('Test failure would be catched', () => {
        fetchMock.get(
            'http://example.com/v1/data',
            {
                body: {
                    error: 'message'
                },
                status: 400
            });
        expect.assertions(2);

        return providerBase.get('/v1/data').catch(({status, body}) => {
            expect(status).toBe(400);
            expect(JSON.parse(body).error).toBe('message');
        });
    });
});


// describe('Test CosmosDX client', () => {
//     const BASE_URL = 'http://cdx-dev.cosmosid.com';
//     const DUMMY_API_KEY = '86f5bfe3-2120-4957-b1c6-6a0384fcc07b';
//     const generate_url = (url) => new URL(url, BASE_URL).href;
//
//     beforeEach(() => {
//         cosmosDXApi.setGlobalConfig({base_url: BASE_URL});
//         cosmosDXApi.setUserData({apiKey: DUMMY_API_KEY});
//
//         fetchMock.restore();
//     });
//
//     it('Works with provided api-key', async () => {
//         const fileId = '81529f38-fa70-4611-927e-15d832255183';
//
//         fetchMock.get((url, { headers }) => generate_url(apiUri.RUNS_BY_FILE(fileId)) === url
//             && headers['X-Api-Key'] === DUMMY_API_KEY, {
//             body: {
//                 runs: []
//             }
//         });
//
//         const runs = await cosmosDXApi.getRunsByFile(fileId);
//         expect(runs.length).toBe(0);
//     });
//
//     it('Gets files per ids (/v2/files/{fileIds})', async () => {
//         const fileIds = ['81529f38-fa70-4611-927e-15d832255183', '1fbc2a5a-8574-43d6-896e-a9cffec2fdfc'];
//
//         fetchMock.get(generate_url(apiUri.GET_FILES(fileIds)), {
//             body: {
//                 // TODO: This test would be updated once /v2/files/{fileIDs} is implemented on backend
//                 files: []
//             }
//         });
//
//         const files = await cosmosDXApi.getFiles(fileIds);
//         expect(files.length).toBe(0);
//     });
//
//     it('Tests getting list of runs for specific file', async () => {
//         const fileId = '412a0c35-4917-4275-b86f-d51ef6cd86f9';
//         const runsList = {'runs': [
//                 {'id': '3ef2377d-2196-4db6-abb1-499efd794485',
//                     'status': 'Success', 'created': '2018-09-14T12:37:03.087595'}]};
//
//         fetchMock.get(generate_url(apiUri.RUNS_BY_FILE(fileId)), {
//             body: runsList
//         });
//
//         const runs = await cosmosDXApi.getRunsByFile(fileId);
//         expect(runs[0].id).toBe('3ef2377d-2196-4db6-abb1-499efd794485');
//     });
//
//     it('allows to get data for single sample run', async () => {
//         const runId = '3ef2377d-2196-4db6-abb1-499efd794485';
//         const runsList = {'id': '3ef2377d-2196-4db6-abb1-499efd794485',
//             'status': 'Success', 'created': '2018-09-14T12:37:03.087595',
//             'file': {'id': '412a0c35-4917-4275-b86f-d51ef6cd86f9', 'name': 'LC100500_.fasta'}};
//
//
//         fetchMock.get(generate_url(apiUri.RUN_INFO(runId)), {
//             body: runsList
//         });
//
//         const run = await cosmosDXApi.getRunInfo(runId);
//         expect(run.id).toBe(runId);
//     });
//
//     it('Gets analysis list for single sample_run', async () => {
//         const runId = '3ef2377d-2196-4db6-abb1-499efd794485';
//
//         fetchMock.get(generate_url(apiUri.ANALYSIS_BY_RUNS(runId)), {
//             body: ANALYSIS_LIST
//         });
//
//         const listOfAnalysis = await cosmosDXApi.getAnalysisListByRun(runId);
//
//         expect(listOfAnalysis.length).toBe(7);
//     });
//     /*
//      * curl https://cdx-dev.cosmosid.com/api/dx/v1/files/412a0c35-4917-4275-b86f-d51ef6cd86f9/analysis/e6f0ea8c-05f6-4679-b541-c87ce24584c5/taxonomy -H 'X-Api-Key: 91461dad-9afb-48bb-a23a-b44d4b9e2a6b'
//      */
//     it('Gets analysis information by file id and analysis id', async () => {
//         const fileId = '412a0c35-4917-4275-b86f-d51ef6cd86f9';
//         const analysisId = 'e6f0ea8c-05f6-4679-b541-c87ce24584c5';
//
//         fetchMock.get(generate_url(apiUri.GET_ANALYSIS_RESULTS_BY_FILE(fileId, analysisId,
//             ANALYSIS_ARTIFACTS.PHYLOGENY.toLowerCase())), { body: TAXONOMY_TREE });
//
//         const analysisInfo = await cosmosDXApi.getAnalysisResults(fileId, analysisId, ANALYSIS_ARTIFACTS.PHYLOGENY);
//
//         expect(analysisInfo.analysis.tax_id).toBe(131567);
//     });
//
//     it('Trying to get wrong artifact', async () => {
//         const fileId = '412a0c35-4917-4275-b86f-d51ef6cd86f9';
//         const analysisId = 'e6f0ea8c-05f6-4679-b541-c87ce24584c5';
//         const resultType = 'WRONG';
//
//         expect.assertions(1);
//
//         try {
//             await cosmosDXApi.getAnalysisResults(fileId, analysisId, resultType);
//         } catch (e) {
//             expect(e).toBe(`${resultType} should be one of ${Object.keys(ANALYSIS_ARTIFACTS)}`);
//         }
//     });
//
//     it('Trying to get artifacts for sample run', async () => {
//         // curl https://cdx-dev.cosmosid.com/api/dx/v1/runs/3ef2377d-2196-4db6-abb1-499efd794485/artifacts -H 'X-Api-Key: 91461dad-9afb-48bb-a23a-b44d4b9e2a6b'
//         const artifactsList = {'artifacts': [{'artifact_type': 'fastqc',
//                 'status_description': 'Artifacts is not available', 'status': 'N/A'}]};
//
//         const runId = '3ef2377d-2196-4db6-abb1-499efd794485';
//
//         fetchMock.get(generate_url(apiUri.SAMPLE_RUN_ARTIFACTS(runId)), { body: artifactsList });
//
//         const artifacts = await cosmosDXApi.getSampleRunArtifacts(runId);
//
//         expect(artifacts[0].artifact_type).toBe('fastqc');
//     });
//
//     it('Trying to get artifact data for sample run', async () => {
//         // curl https://cdx-dev.cosmosid.com/api/dx/v1/runs/3ef2377d-2196-4db6-abb1-499efd794485/artifacts -H 'X-Api-Key: 91461dad-9afb-48bb-a23a-b44d4b9e2a6b'
//
//         const runId = '3ef2377d-2196-4db6-abb1-499efd794485';
//
//         fetchMock.get(generate_url(apiUri.SAMPLE_RUN_ARTIFACT_DATA(runId, SAMPLE_RUN_ARTIFACTS.FASTQC.toLowerCase())),
//             { body: {data: 'something'} });
//
//         const artifact = await cosmosDXApi.getSampleRunArtifactData(runId, SAMPLE_RUN_ARTIFACTS.FASTQC);
//
//         expect(artifact.data).toBe('something');
//     });
//
//     it('Error when trying to get artifact that is not allowed', async () => {
//         // curl https://cdx-dev.cosmosid.com/api/dx/v1/runs/3ef2377d-2196-4db6-abb1-499efd794485/artifacts -H 'X-Api-Key: 91461dad-9afb-48bb-a23a-b44d4b9e2a6b'
//
//         const runId = '3ef2377d-2196-4db6-abb1-499efd794485';
//         const resultType = 'WRONG';
//
//         expect.assertions(1);
//
//         try {
//             await cosmosDXApi.getSampleRunArtifactData(runId, resultType);
//         } catch (e) {
//             expect(e).toBe(`${resultType} should be one of ${Object.keys(SAMPLE_RUN_ARTIFACTS)}`);
//         }
//
//     });
//
//     it('Creates file', async () => {
//         const fileId = '412a0c35-4917-4275-b86f-d51ef6cd86f9';
//
//         fetchMock.post((url, {body}) => {
//             return generate_url(apiUri.CREATE_FILE()) && body['name'] === 'some.fasta';
//         }, {
//             body: {created: [fileId]}
//         });
//
//         const created = await cosmosDXApi.createFile({name: 'some.fasta'});
//         expect(created).toBe(fileId);
//     });
// });