<?php

$dirPublish=$argv[1];
$updateServer=$argv[2];
$version=$argv[3];

if($version == ""){
	sprint("请输入版本号：");
	$input = trim(fgets(STDIN));
	
	if($input == "")
		$version = "1.0.0.0";
	else {
		$version = $input;
	}
}

$resfilelist = tree($dirPublish."/res");
$srcfilelist = tree($dirPublish."/src");
$filelist = array_merge_recursive($resfilelist,$srcfilelist);

$versionfile = fopen("version.txt", "w");
fwrite($versionfile, $version);
$vfile = fopen($dirPublish."/version.manifest", "w");
$pfile = fopen($dirPublish."/project.manifest", "w");

$headStr = '{
"packageUrl" : "'.$updateServer.'",
"remoteVersionUrl" : "'.$updateServer.'version.manifest",
"remoteManifestUrl" : "'.$updateServer.'project.manifest",
"version" : "'.$version.'",
"engineVersion" : "Cocos2d-JS v3.10.1"';

fwrite($vfile, $headStr."\n}");
fwrite($pfile, $headStr.',
"assets" : {');
$index = 0;
foreach ($filelist as $file){
	$index ++;
	$str = '
	"'.substr($file, strlen($dirPublish)+1).'" : {
		"md5" : "'.md5_file($file).'",
		"size" : '.filesize($file).'
	}';
	if($index<sizeof($filelist))
		$str .= ',';
	fwrite($pfile, $str);
}
fwrite($pfile, "\n\t}\n}");

function tree($directory)
{
	$filelist = array();
    $mydir = dir($directory);
    while($file = $mydir->read())
    	if((is_dir("$directory/$file")) AND ($file!=".") AND ($file!=".."))
            $filelist = array_merge_recursive($filelist,tree("$directory/$file"));
        else if (($file!=".") AND ($file!="..") AND ($file!=".DS_Store") AND (substr($file,0,2)!="._") AND ($file!="logo.png") AND ($file!="bg_018.jpg") AND ($file!="favicon.png"))
        	array_push($filelist,"$directory/$file");
    $mydir->close();
    return $filelist;
}

function sprint($text) {
	if(PHP_OS=="WINNT")
		echo $text;
	else
		echo(chr(27) . "[35m" . "$text" . chr(27) . "[0m");
}

function println($text) {
	if(PHP_OS=="WINNT")
		echo $text."\n";
	else
		echo(chr(27) . "[35m" . "$text" . chr(27) . "[0m\n");
}

function error($text) {
	if(PHP_OS=="WINNT")
		echo $text."\n";
	else
		echo(chr(27) . "[31m" . "$text" . chr(27) . "[0m\n");
}

function success($text) {
	if(PHP_OS=="WINNT")
		echo $text."\n";
	else
		echo(chr(27) . "[32m" . "$text" . chr(27) . "[0m\n");
}
?>
