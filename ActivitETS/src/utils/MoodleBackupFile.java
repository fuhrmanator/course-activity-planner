package utils;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import org.apache.commons.compress.archivers.ArchiveEntry;
import org.apache.commons.compress.archivers.ArchiveException;
import org.apache.commons.compress.archivers.ArchiveInputStream;
import org.apache.commons.compress.archivers.ArchiveStreamFactory;
import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream;
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveInputStream;
import org.apache.commons.compress.archivers.zip.ZipFile;
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream;
import org.apache.commons.io.IOUtils;

public class MoodleBackupFile {

	/**
	 * Size of the buffer to read/write data
	 */
	private static final int BUFFER_SIZE = 4096;
	private ArrayList<String> fileList = new ArrayList<String>();
    private static final String OUTPUT_ZIP_FILE = "MyFile.mbz";
    private static final String SOURCE_FOLDER = "MoodleBackup\\\\";
	/**
	 * Extracts a zip file specified by the zipFilePath to a directory specified
	 * by destDirectory (will be created if does not exists)
	 * 
	 * @param zipFilePath
	 * @param destDirectory
	 * @throws IOException
	 */
    
    final String OUTPUT_FOLDER = "dest";
    
    public void unzip(String file, String destDirectory) throws FileNotFoundException, IOException, ArchiveException {
 
        File inputFile = new File(file);
        //ZipFile zipFile = new ZipFile(file);
        
        //InputStream is = new FileInputStream(inputFile);
        //ArchiveInputStream ais = new ArchiveStreamFactory().createArchiveInputStream(ArchiveStreamFactory.ZIP, is);
        //ZipEntry entry = null;
        try {
        	 FileInputStream fin = new FileInputStream(inputFile);
             BufferedInputStream in = new BufferedInputStream(fin);
             GzipCompressorInputStream gzIn = new GzipCompressorInputStream(in);
             TarArchiveInputStream tarIn = new TarArchiveInputStream(gzIn);
             TarArchiveEntry entry = null;

             
             File dirMoodleBackup = new File(destDirectory);
             if (!dirMoodleBackup.exists()) {
             	dirMoodleBackup.mkdirs();
             }
             
             while ((entry = (TarArchiveEntry) tarIn.getNextEntry()) != null) {
      
                 if (entry.getName().endsWith("/")) {
                     File dir = new File(destDirectory + File.separator + entry.getName());
                     if (!dir.exists()) {
                         dir.mkdirs();
                     }
                     continue;
                 }
      
                 File outFile = new File(destDirectory + File.separator + entry.getName());
      
                 if (outFile.isDirectory()) {
                     continue;
                 }
      
                 if (outFile.exists()) {
                     continue;
                 }
      
                 FileOutputStream out = new FileOutputStream(outFile);
                 byte[] buffer = new byte[1024];
                 int length = 0;
                 while ((length = tarIn.read(buffer)) > 0) {
                     out.write(buffer, 0, length);
                     out.flush();
                 }
      
             }
        } catch(FileNotFoundException e) {
        	
        }
       
    }
    
    
	/*public void unzip(String zipFilePath, String destDirectory)
			throws IOException {

		// InputStream is = new GZIPInputStream(new
		// FileInputStream(zipFilePath));

		File destDir = new File(destDirectory);
		if (!destDir.exists()) {
			destDir.mkdir();
		}
		//ZipFile zipFile = new ZipFile(new File(zipFilePath));
		ZipArchiveInputStream zipIn = new ZipArchiveInputStream(new FileInputStream(
				zipFilePath));
		
		//ArrayList<ZipArchiveEntry> zipArchiveEntry =  (ArrayList<ZipArchiveEntry>) zipFile.getEntries();
		
		//System.out.println("test : " + zipArchiveEntry.size());
		//InputStream is  = zipFile.getInputStream(zipArchiveEntry);
		ArchiveEntry entry = zipIn.getNextEntry();
		//ZipArchiveEntry test =  zipIn.getNextZipEntry();
		// iterates over entries in the zip file
		//System.out.println(test.getCompressedSize());
		while (entry != null) {
			String filePath = destDirectory + File.separator + entry.getName();
			if (!entry.isDirectory()) {
				// if the entry is a file, extracts it
				extractFile(zipIn, filePath);
			} else {
				// if the entry is a directory, make the directory
				File dir = new File(filePath);
				dir.mkdir();
			}
			//zipIn.close();
			entry = zipIn.getNextEntry();
		}
		zipIn.close();
		//zipFile.close();
	}*/

	/**
	 * Extracts a zip entry (file entry)
	 * 
	 * @param zipIn
	 * @param filePath
	 * @throws IOException
	 */
	private void extractFile(ZipArchiveInputStream zipIn, String filePath)
			throws IOException {
		BufferedOutputStream bos = new BufferedOutputStream(
				new FileOutputStream(filePath));
		byte[] bytesIn = new byte[BUFFER_SIZE];
		int read = 0;
		while ((read = zipIn.read(bytesIn)) != -1) {
			bos.write(bytesIn, 0, read);
		}
		bos.close();
	}

	
	
	
	
	/*
	 * 
	 * 
	 * ZIP FILES
	 * 
	 * 
	 */
	
	public void zipIt(String zipFile) {

		generateFileList(new File(SOURCE_FOLDER));
		
		byte[] buffer = new byte[1024];

		try {

			FileOutputStream fos = new FileOutputStream(zipFile);
			ZipOutputStream zos = new ZipOutputStream(fos);

			System.out.println("Output to Zip : " + zipFile);

			for (String file : this.fileList) {

				System.out.println("File Added : " + file);
				ZipEntry ze = new ZipEntry(file);
				zos.putNextEntry(ze);

				FileInputStream in = new FileInputStream(SOURCE_FOLDER
						+ File.separator + file);

				int len;
				while ((len = in.read(buffer)) > 0) {
					zos.write(buffer, 0, len);
				}

				in.close();
			}

			zos.closeEntry();
			// remember close it
			zos.close();

			System.out.println("Done");
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}

	public void generateFileList(File node) {

		// add file only
		if (node.isFile()) {
			fileList.add(generateZipEntry(node.getAbsoluteFile().toString()));
		}

		if (node.isDirectory()) {
			String[] subNote = node.list();
			for (String filename : subNote) {
				generateFileList(new File(node, filename));
			}
		}

	}

    private String generateZipEntry(String file){
    	
    	String test = file.split(SOURCE_FOLDER)[1];
    	/*if(test.startsWith("\\")) {
    		test = test.split("\\")[1];
    	}*/
    	return test;
    }
}
