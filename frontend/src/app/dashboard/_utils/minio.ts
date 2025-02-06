'use server'
var Minio = require("minio");

var client = new Minio.Client({
    endpoint:  'play.min.io',
    port:       9000,
    useSSL:     true,
    accessKey:  'Q3AM3UQ867SPQQA43P2F',
    secretKey:  'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
})


  const uploadFileToMinio = async (file: File, buffer: Buffer, fileName: string, fileType: string) => {
    try {
      const etag = await new Promise((resolve, reject) => {
        client.putObject(
          'my-bucket',
          fileName,
          buffer,
          buffer.length,
          { 'Content-Type': fileType },
        );
      });
      console.log('Upload successful:', etag);
    } catch (error) {
      console.error('Upload failed', error);
      throw error;
    }
  };


  export { uploadFileToMinio };