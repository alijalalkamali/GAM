import com.clearnlp.nlp.NLPGetter;
import com.clearnlp.reader.AbstractReader;
import com.clearnlp.segmentation.AbstractSegmenter;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.simple.Document;
import edu.stanford.nlp.simple.Sentence;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class TokenizerComparer {

    private static Set<String> filenameList = new HashSet<>();

    public static void main(String[] args) throws IOException {

        String stateWordFile;
        String stativeVerbFile;
        
        String inputFileDir;
        String outputFile;
        String isSkip;

        try {
            stateWordFile = args[0];
            stativeVerbFile = args[1];
            inputFileDir = args[2];
            outputFile = args[3];
            isSkip = args[4];
        } catch (Exception e) {
            System.out.println("Please input following arguments [stateWordFilePath] [stativeVerbFilePath] [inputDirPath] [outputFilePath] [isSkipSame]");
            throw e;
        }

        Set<String> stateWordList = new HashSet<>();
        try {
            stateWordList = readListFromFile(stateWordFile);
        } catch (Exception e) {
            System.out.println("Missing state word list file!");
            throw e;
        }

        Set<String> stativeVerbList = new HashSet<>();
        try {
            stativeVerbList = readListFromFile(stativeVerbFile);
        } catch (Exception e) {
            System.out.println("Missing stative verb list file!");
            throw e;
        }


        TokenizerComparer comparer = new TokenizerComparer();

        File inputDir = new File(inputFileDir);


        for (File file : Objects.requireNonNull(inputDir.listFiles())) {
            if (file.isFile() && file.getName().endsWith(".txt") && file.getName().contains("newsText")) {
                try {
                    String content = new Scanner(file).useDelimiter("\\Z").next();
                    Document doc = new Document(content);

                    boolean hasState = false;
                    boolean hasVerb = false;

                    for (Sentence sent : doc.sentences()) {
                        for (String lemma : sent.lemmas()) {
                            if (!hasVerb && stativeVerbList.contains(lemma)) {
                                hasVerb = true;
                            }
                            if (!hasState && stateWordList.contains(lemma)) {
                                hasState = true;
                            }

                            if (hasVerb && hasState) {
                                break;
                            }
                        }
                        if (hasVerb && hasState) {
                            break;
                        }
                    }

                    if (hasState && hasVerb) {
                        if (isSkip.equals("1")) {
                            comparer.processFile(file.getAbsoluteFile());
                        } else {
                            filenameList.add(file.getCanonicalPath());
                        }
                    }
                } catch (Exception e) {
                    System.out.println("[Skipped] " + file.getCanonicalPath());
                }
            }
        }

        try (PrintWriter out = new PrintWriter(outputFile)) {
            for (String filename : filenameList) {
                out.println(filename);
            }
        }

    }

    private static Set<String> readListFromFile(String filename) throws FileNotFoundException {
        Set<String> fileset = new HashSet<>();

        Scanner s = new Scanner(new File(filename));
        while (s.hasNext()) {
            fileset.add(s.next());
        }
        s.close();

        return fileset;
    }

    private void processFile(File inputFile) throws IOException {
        final String language = AbstractReader.LANG_EN;
        AbstractSegmenter segmenter	 = NLPGetter.getSegmenter(language, NLPGetter.getTokenizer(language));

        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile)));
        Iterator<List<String>> tokens = segmenter.getSentences(reader).iterator();
        reader.close();

        DocumentPreprocessor dp = new DocumentPreprocessor(String.valueOf(inputFile));
        Iterator<List<HasWord>> corenlpTokens = dp.iterator();

        if (!compareTokens(tokens, corenlpTokens)) {
            filenameList.add(inputFile.toString());
        }
    }

    private static boolean compareTokens(Iterator<List<String>> t1, Iterator<List<HasWord>> t2) {
        while (t1.hasNext() && t2.hasNext()) {
            List<String> i1 = t1.next();
            List<String> i2 = t2.next().stream().map(HasWord::word).collect(Collectors.toList());

//            if (i1.size() != i2.size()) return false;
//            for (int i = 0; i < i1.size(); i++) {
//                if (!i1.get(i).equals(i2.get(i))) {
//                    System.out.println(i1.get(i));
//                    System.out.println(i2.get(i));
//                }
//            }

            if (!i1.equals(i2)) {
                return false;
            }
        }

        return !t1.hasNext() && !t2.hasNext();
    }

}
