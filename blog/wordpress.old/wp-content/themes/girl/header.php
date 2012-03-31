<?php load_theme_textdomain('girl');?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>
<head>
	<title><?php wp_title(); ?> <?php bloginfo('name'); ?></title>
	<style type="text/css" media="screen">
		@import url( <?php bloginfo('stylesheet_url'); ?> );
	</style>

	<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />

	<?php
	if ( is_singular() ) wp_enqueue_script( 'comment-reply' );
	wp_head();
	?>

</head>
<body <?php body_class(); ?>>


<div class="blogname"><a class="blognamelink" href="<?php echo home_url( '/' ); ?>"><?php bloginfo('name'); ?></a></div>
<div class="main">

<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
